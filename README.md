# oitrainslate
Self hosted system to send alerts when your train is delayed.

## Objectives
- Provide a self-hosted solution for sending alerts when trains are delayed.
- Initially support only one train journey.
- Haven't decided on the notification method yet.

## Release 1 - Simple Command Line Tool

The first release will require python and will run with pipx. 

The only functionality will be to accept a starting and destination station and return the expected and
actual departure times for services between those stations.

Example usage: `pipx run oitrainslate BWD URM`