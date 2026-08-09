### Requirements List

1. Tag v0.1 Create a db for all the timer logs, so that it can track the time consumed by the scraper
2. Tag v0.2 Ensure that the html tags aren't being generated for the jds
3. Tag v0.3 Added the normalization function to the diff and main
4. Tag v0.4 Optimized the main logic to make things more readable and simpler at the same time
5. Tag v0.5 Prevent silent database resets on corrupted JSON
6. Tag v1.0 Implemented job history tracking database
7. Tag v1.1 Added the Universally Unique ID (UUID) to the jsonls, timer db and history db
8. Tag v1.2 Added the feature to allow querying the logs db from cli
9. Tag v1.3 Renamed "run_uuid" to uuid
10. Tag v1.4 Added the Q initializer and created the architecture for the jd workers
11. Tag v1.5 Cleaned up main, and added an email handler via the logging system
12. Tag v2.0 Added the JD worker