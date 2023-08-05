def daily_publisher_revenue(ads_csv_name, publisher_csv_name):
    # import os to be able to read the current working directory
    import os
    wd_files = [f.upper() for f in os.listdir('.') if os.path.isfile(f)]

    # Checking whether the files are the in the working directory
    required_files = [ads_csv_name.upper(), publisher_csv_name.upper()]
    if all(req_file in wd_files for req_file in required_files):

        # Only importing pandas when file names are actually present.
        # Only importing the necessary functions from pandas rather than whole library
        from pandas import read_csv, merge

        # Join the two CSVs but only keeping DATE, PUB_NAME and REVENUE
        csv_join = read_csv(ads_csv_name).merge(read_csv(publisher_csv_name), left_on='PUBLISHER_ID', right_on='ID')[
            ['DATE', 'NAME', 'REVENUE']].rename(columns={'NAME': 'PUBLISHER_NAME'})

        # Perform a group by on DATE and PUB_NAME summing the revenue
        csv_group = csv_join.groupby(['DATE', 'PUBLISHER_NAME'])['REVENUE'].sum()

        # Looping through the items of the resulting group by to print the desired output
        print(csv_group.index.names[0], csv_group.index.names[1], csv_group.name, sep=',')
        for index in csv_group.index:
            print(index[0], index[1], csv_group[index], sep=',')

    # If files are not present in working directory raise an error
    else:
        raise ValueError('One or more items are missing of the following:', required_files)