import pandas as pd
from models import CarMake, CarModel, InsuranceClass, InsuranceSubclass, Constituency, County, Ward


# Import the CSV files into python using read_csv

# fetch car makes data and send it to its models
def car_makes():
    df = pd.read_csv("data/Car_Makes_Insurance.csv")
    for row in df.head().itertuples():
        new_car_make = CarMake(row.Make_ID, row.Make_Name)
        new_car_make.save()

# fetch car models data
def car_models():
    df = pd.read_csv("data/Car_Models_Insurance.csv")
    for row in df.head().itertuples():
        # TODO: get car make by name
        car_make = CarMake.get_car_make_by_name(row.Make_Name)
        new_car_model = CarModel(row.Model_Name, row.Series, car_make)
        new_car_model.save()

# Insurance classes and subclasses
def insurance_classes():
    df = pd.read_csv("data/Classes_Insurance.csv")
    for row in df.head().itertuples():
        # Generate acronym
        # declare empty variable to store acronym
        acronym = None
        if row.Class_Insurance == 'Aviation':
            acronym = 'AVI'
        elif row.Class_Insurance == 'Engineering':
            acronym = 'ENG'
        elif row.Class_Insurance == 'Fire Domestic':
            acronym = 'FDH'
        elif row.Class_Insurance == 'Liability':
            acronym = 'LIB'
        elif row.Class_Insurance == 'Marine':
            acronym = 'MAR'
        elif row.Class_Insurance == 'Motor Private':
            acronym = 'MPI'
        elif row.Class_Insurance == 'Motor Commercial':
            acronym = 'MCI'
        elif row.Class_Insurance == 'Personal Accident':
            acronym = 'PAI'
        elif row.Class_Insurance == 'Theft':
            acronym = 'TFT'
        elif row.Class_Insurance == 'Workmen Compensation':
            acronym = 'WCA'
        elif row.Class_Insurance == 'Medical':
            acronym = 'MDI'
        elif row.Class_Insurance == 'Miscellaneous':
            acronym = 'MIS'

        # Create a new insurance class
        new_insurance_class = InsuranceClass(
            row.Serial_Number, row.Class_Insurance, acronym, row.Sector)
        new_insurance_class.save()

        # create subclass, Note that we've used the serial number as the foreign key for the related insurance class
        new_sub_class = InsuranceSubclass(
            row.Class_Code, row.Subclasses, row.Serial_Number)
        new_sub_class.save()

# Counties
def counties():
    df = pd.read_csv("data/County_Insurance.csv")
    for row in df.head().itertuples():
        new_county = County(row.County_Name)
        new_county.save()

def constituencies():
    df = pd.read_csv("data/Constituency_Insurance.csv")

    for row in df.head().itertuples():
        # TODO: Create get county by name
        county = County.get_county_by_name(row.County_Name)
        new_constituency = Constituency(row.Constituency_Name, county)
        new_constituency.save()

def ward():
    df = pd.read_csv("data/Ward_Insurance.csv")
    for row in df.head().itertuples():
        county_id = County.get_county_by_name(row.County_Name)
        new_ward = Ward(row.Ward_Name, row.Constituency_Code, county_id)
        new_ward.save()

if __name__ == '__main__':
    car_makes()
    car_models()
    insurance_classes()
    counties()
    constituencies()
    ward()
