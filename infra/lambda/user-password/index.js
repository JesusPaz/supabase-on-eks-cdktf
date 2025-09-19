const { SecretsManagerClient, GetSecretValueCommand, PutSecretValueCommand } = require('@aws-sdk/client-secrets-manager');
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

/** Put secret to Secrets Manager */
const putSecret = async (secretId, SecretValue) => {
  const cmd = new PutSecretValueCommand({ SecretId: secretId, SecretString: JSON.stringify(SecretValue) });
  await secretsManager.send(cmd);
};

/** Escape a parameter for DDL */
const raw = (text) => sql.__dangerous__rawValue(text);

/** Set password */
const setUserPassword = async (db, username, password) => {
  await db.query(sql`ALTER USER ${raw(username)} WITH PASSWORD ${raw(password)}`);
};

exports.handler = async (event, _context) => {
  /** The name of user to be created or dropped */
  const username = event.ResourceProperties.Username;
  /** The secret of user to be created */
  const secretId = event.ResourceProperties.SecretId;

  /** The secret used for database connections */
  const dbSecret = await getSecret(dbSecretArn);
  const { host, port, dbname, username: rootUsername, password: rootPassword } = dbSecret;

  /** Database connection */
  const db = connect({
    host,
    port: Number(port),
    user: rootUsername,
    password: rootPassword,
    database: dbname || 'postgres',
    ssl: 'disable',
  });
  console.log('Connected to PostgreSQL database');

  let physicalResourceId;

  switch (event.RequestType) {
    case 'Create': {
      const { password } = await getSecret(secretId);
      await setUserPassword(db, username, password);
      await putSecret(secretId, {
        ...dbSecret,
        username,
        password,
        uri: `postgres://${username}:${password}@${host}:${port}/${dbname}`,
      });
      physicalResourceId = `${username}@${dbSecret.host}`;
      break;
    }
    case 'Update': {
      const { password } = await getSecret(secretId);
      await setUserPassword(db, username, password);
      await putSecret(secretId, {
        ...dbSecret,
        username,
        password,
        uri: `postgres://${username}:${password}@${host}:${port}/${dbname}`,
      });
      physicalResourceId = `${username}@${dbSecret.host}`;
      break;
    }
    case 'Delete': {
      break;
    }
  }

  await db.dispose();
  return { PhysicalResourceId: physicalResourceId };
};