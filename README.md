# logParserWeb
Webapp for the anomaly detection project.
# Instructions
  Create the parsedOutput and uploadedLogs folder<br>
  Before running:<br>
  `pip install -r requirements.txt`<br>
  To run the server:<br>
    `cd logParserWeb` <br>
    `python server.py`<br>
  To upload the file visit localhost:5000<br>

# Current functionality in the webapp:
  1. File upload from web interface.
  2. Generating parsed file and saving it.
  3. Getting the unique IP list.
  4. Calculating outliers based on IQR and sending data of the same.(outliers and inliers)
    - Tunable parameter :
      - Alpha (Floating point value)
  5. Calculating outliers based on moving window MAD and sending data of the same.(outliers and inliers)
    - Tunable parameters:
      - Alpha (Floating point value)
      - Window Size (Integer value)
  6. Calculating outliers based on Moving Average and sending data of the same.(outliers and inliers)
    - Tunable parameters:
      - Window Size (Integer value)
