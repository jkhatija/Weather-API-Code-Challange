import os
import dask.dataframe as daskDataFrame
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define a Base class and create an engine to connect to an SQLite database
Base = declarative_base()
engine = create_engine('sqlite:///weather.db', echo=True)
Base.metadata.create_all(bind=engine)

# Define a session maker to create a session object that can interact with the database
Session = sessionmaker(bind=engine)

# Define a function to ingest weather data from a directory


def data_ingestion(directory):
    dataframes = []

    # Iterate through all files in the specified directory
    for file_data in os.listdir(directory):
        if file_data.endswith(".txt"):
            filepath = os.path.join(directory, file_data)

            # Read the data from the file into a Dask dataframe
            data = daskDataFrame.read_csv(filepath, sep="\t", header=None,
                                          names=["date", "max_temp", "min_temp", "precipitation"])

            # Append the dataframe to the list of dataframes
            data["Station_ID"] = file_data[:11]
            dataframes.append(data)

    # Concatenate all dataframes in the list into a single dataframe
    data = daskDataFrame.concat(dataframes)

    # Compute the dataframe (i.e., load it into memory)
    data = data.compute()
    data = data.reset_index(drop=True)

    # Remove any rows with missing temperature or precipitation data
    result = data[(data['max_temp'] != -9999) |
                  (data['min_temp'] != -9999) | (data['precipitation'] != -9999)]

    # Group the data by station ID and year, and compute the mean maximum and minimum temperatures
    # and the total accumulated precipitation for each group
    result = result.groupby(['Station_ID', data['date'].map(str).str[:4]]).agg({
        'max_temp': 'mean',
        'min_temp': 'mean',
        'precipitation': 'sum'
    }).reset_index()

    # Rename the columns to more descriptive names
    heading = {'max_temp': 'AvgMaxtemp', 'min_temp': 'AvgMintemp',
               'precipitation': 'TotalAccPrecipitation'}
    result.rename(columns=heading, inplace=True)

    # Establish a connection to the database and create a session object
    session = engine.raw_connection()

    # Write the weather data to a table in the database
    data.to_sql("weather_records", session, if_exists="replace",
                index=True, index_label='id')
    result.to_sql("weather_stats", session, if_exists="replace",
                  index=True, index_label='id')

    # Commit the changes to the database and close the session
    session.commit()
    session.close()


# Call the dataIngestion function with the specified directory
data_ingestion('../wx_data')
