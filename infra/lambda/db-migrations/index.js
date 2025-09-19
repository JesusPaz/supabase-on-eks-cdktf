const fs = require('fs');
const https = require('https');
const url = require('url');
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');
const connect = require('@databases/pg');
const { sql } = require('@databases/pg');

const dbSecretArn = process.env.DB_SECRET_ARN;

/** API Client for Secrets Manager */
const secretsManager = new SecretsManagerClient({});

/** Get secret from Secrets Manager */
const getSecret = async (secretId) => {
  const cmd = new GetSecretValueCommand({ SecretId: secretId });
  const { SecretString } = await secretsManager.send(cmd);
  const secret = JSON.parse(SecretString);
  return secret;
};

/** Send response to CloudFormation */
const sendResponse = async (event, context, status, data = {}, physicalResourceId = null) => {
  const responseBody = JSON.stringify({
    Status: status,
    Reason: data.Reason || `See CloudWatch Log Stream: ${context.logStreamName}`,
    PhysicalResourceId: physicalResourceId || context.logStreamName,
    StackId: event.StackId,
    RequestId: event.RequestId,
    LogicalResourceId: event.LogicalResourceId,
    Data: data
  });

  console.log('Sending response:', responseBody);

  const parsedUrl = url.parse(event.ResponseURL);
  const options = {
    hostname: parsedUrl.hostname,
    port: 443,
    path: parsedUrl.path,
    method: 'PUT',
    headers: {
      'content-type': '',
      'content-length': responseBody.length
    }
  };

  return new Promise((resolve, reject) => {
    const request = https.request(options, (response) => {
      console.log('Response status code:', response.statusCode);
      resolve();
    });

    request.on('error', (error) => {
      console.error('Error sending response:', error);
      reject(error);
    });

    request.write(responseBody);
    request.end();
  });
};

/** Run queries under the directory */
const runQueries = async (db, dir) => {
  try {
    console.info(`Processing directory: ${dir}`);
    
    // Check if directory exists
    if (!fs.existsSync(dir)) {
      console.warn(`Directory does not exist: ${dir}`);
      return;
    }

    /** SQL files under the directory */
    const files = fs.readdirSync(dir).filter(name => name.endsWith('.sql'));
    console.info(`Found ${files.length} SQL files in ${dir}`);

    for (const file of files.sort()) {
      const filePath = `${dir}/${file}`;
      try {
        console.info(`Executing SQL file: ${filePath}`);
        const query = sql.file(filePath);
        const result = await db.query(query);
        console.info(`Successfully executed: ${file}`);
        if (result.length > 0) {
          console.info(`Query returned ${result.length} rows`);
        }
      } catch (err) {
        // Handle common idempotent errors that are safe to ignore
        if (err.message.includes('already exists') || 
            err.message.includes('already installed') ||
            err.message.includes('permission denied to set parameter') ||
            err.message.includes('does not exist') && (err.message.includes('role') || err.message.includes('function')) ||
            err.message.includes('relation') && err.message.includes('already exists')) {
          console.warn(`Skipping ${file} - resource already exists, permission denied, or missing dependency: ${err.message}`);
        } else {
          console.error(`Error executing ${file}:`, err.message);
          throw err; // Re-throw to stop execution on error
        }
      }
    }
  } catch (err) {
    console.error(`Error processing directory ${dir}:`, err.message);
    throw err;
  }
};

exports.handler = async (event, context) => {
  console.info('Lambda invoked with event:', JSON.stringify(event, null, 2));
  console.info('Lambda context:', JSON.stringify(context, null, 2));
  
  try {
    // Only run migrations for CloudFormation Custom Resource events
    if (event.RequestType) {
      const dbSecret = await getSecret(dbSecretArn);
      
      // RDS auto-generated secrets only contain username and password
      // We need to get host from environment or construct it
      const { username: rootUsername, password: rootPassword } = dbSecret;
      
      // Get RDS endpoint from environment variable
      const host = process.env.DB_HOST;
      const port = 5432;
      const dbname = 'supabase';

      console.info(`Connecting to database: ${host}:${port}/${dbname}`);
      
      const db = connect({
        host,
        port: Number(port),
        user: rootUsername,
        password: rootPassword,
        database: dbname,
        ssl: 'disable',
        bigIntMode: 'number',
      });
      console.info('Connected to PostgreSQL database');

      try {
        switch (event.RequestType) {
          case 'Create':
          case 'Update': {
            console.info('Running database migrations...');
            await runQueries(db, './sql/init-for-rds/');
            await runQueries(db, './sql/init-scripts/');
            await runQueries(db, './sql/migrations/');
            console.info('Database migrations completed successfully');
            break;
          }
          case 'Delete': {
            console.info('Delete operation - no action required');
            break;
          }
          default: {
            console.warn(`Unknown RequestType: ${event.RequestType}`);
            break;
          }
        }
      } finally {
        await db.dispose();
        console.info('Database connection closed');
      }
      
      // Send SUCCESS response to CloudFormation
      await sendResponse(event, context, 'SUCCESS', {
        Message: 'Database migrations completed successfully'
      });
    } else {
      console.info('Direct Lambda invocation - not a CloudFormation event');
    }
    
    return { statusCode: 200, body: 'Success' };
  } catch (error) {
    console.error('Lambda execution failed:', error);
    
    // Send FAILED response to CloudFormation if this is a CF event
    if (event.RequestType) {
      try {
        await sendResponse(event, context, 'FAILED', {
          Reason: error.message
        });
      } catch (responseError) {
        console.error('Failed to send error response to CloudFormation:', responseError);
      }
    }
    
    throw error;
  }
};