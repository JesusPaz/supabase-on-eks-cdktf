{{/*
Expand the name of the chart.
*/}}
{{- define "supabase.auth.name" -}}
{{- default (print .Chart.Name "-auth") .Values.auth.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "supabase.auth.fullname" -}}
{{- if .Values.auth.fullnameOverride }}
{{- .Values.auth.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default (print .Chart.Name "-auth") .Values.auth.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "supabase.auth.selectorLabels" -}}
app.kubernetes.io/name: {{ include "supabase.auth.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "supabase.auth.serviceAccountName" -}}
{{- if .Values.auth.serviceAccount.create }}
{{- default (include "supabase.auth.fullname" .) .Values.auth.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.auth.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Construct DATABASE_URL for Auth
*/}}
{{- define "supabase.auth.databaseUrl" -}}
{{- $host := "" -}}
{{- $port := include "supabase.db.port" . -}}
{{- $sslmode := include "supabase.db.sslmode" . -}}
{{- if .Values.db.enabled -}}
{{- $host = include "supabase.db.fullname" . -}}
{{- else -}}
{{- $host = "$(GOTRUE_DB_HOST)" -}}
{{- end -}}
postgres://$(GOTRUE_DB_USER):$(GOTRUE_DB_PASSWORD)@{{ $host }}:{{ $port }}/$(GOTRUE_DB_NAME)?search_path=auth&sslmode={{ $sslmode }}
{{- end }}