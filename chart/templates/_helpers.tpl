{{/*
Expand the name of the chart.
*/}}
{{- define "qbooks.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "qbooks.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "qbooks.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "qbooks.labels" -}}
helm.sh/chart: {{ include "qbooks.chart" . }}
{{ include "catalog.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Catalog selector labels
*/}}
{{- define "catalog.selectorLabels" -}}
app.kubernetes.io/name: {{ include "qbooks.name" . }}-catalog
app.kubernetes.io/instance: {{ .Release.Name }}
app: qbooks
version: 0.0.1
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "frontend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "qbooks.name" . }}-frontend
app.kubernetes.io/instance: {{ .Release.Name }}
app: qbooks
version: 0.0.1
{{- end }}

{{/*
Admin selector labels
*/}}
{{- define "admin.selectorLabels" -}}
app.kubernetes.io/name: {{ include "qbooks.name" . }}-admin
app: qbooks
version: 0.0.1
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
recommendator selector labels
*/}}
{{- define "recommendator.selectorLabels" -}}
app.kubernetes.io/name: {{ include "qbooks.name" . }}-recommendator
app.kubernetes.io/instance: {{ .Release.Name }}
app: qbooks
version: 0.0.1
{{- end }}

{{/*
Api gateway selector labels
*/}}
{{- define "apiGateway.selectorLabels" -}}
app.kubernetes.io/name: {{ include "qbooks.name" . }}-api-gateway
app.kubernetes.io/instance: {{ .Release.Name }}
app: qbooks
version: 0.0.1
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "qbooks.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "qbooks.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
