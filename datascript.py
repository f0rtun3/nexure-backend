import pandas as pd
from models import CarMake, CarModel, InsuranceClass, InsuranceSubclass, Constituency, County, Ward

# Import the CSV files into python using read_csv
# fetch car makes data and send it to its models


def car_makes():
    df = pd.read_csv("data/Car_Makes_Insurance.csv")
    for row in df.itertuples():
        new_car_make = CarMake(row.Make_ID, row.Make_Name)
        new_car_make.save()

# fetch car models data


def car_models():
    df = pd.read_csv("data/clean_car_models.csv")
    for row in df.itertuples():
        # TODO: get car make by name
        car_make = CarMake.get_car_make_by_name(row.Make_Name)
        new_car_model = CarModel(row.Model_Name, row.Series, car_make)
        new_car_model.save()

# Insurance classes and subclasses


def insurance_classes():
    df = pd.read_csv("data/cleaned_classes.csv")
    for row in df.itertuples():
        # Generate acronym
        # declare empty variable to store acronym
        acronym = None
        class_id = None
        if row.Class_Insurance == 'Aviation':
            acronym = 'AVI'
            class_id = '01'
        elif row.Class_Insurance == 'Engineering':
            acronym = 'ENG'
            class_id = '02'
        elif row.Class_Insurance == 'Fire Domestic':
            acronym = 'FDH'
            class_id = '03'
        elif row.Class_Insurance == 'Fire Industrial':
            acronym = 'FID'
            class_id = '04'
        elif row.Class_Insurance == 'Liability':
            acronym = 'LIB'
            class_id = '05'
        elif row.Class_Insurance == 'Marine':
            acronym = 'MAR'
            class_id = '06'
        elif row.Class_Insurance == 'Motor Private':
            acronym = 'MPI'
            class_id = '07'
        elif row.Class_Insurance == 'Motor Commercial':
            acronym = 'MCI'
            class_id = '08'
        elif row.Class_Insurance == 'Personal Accident':
            acronym = 'PAI'
            class_id = '09'
        elif row.Class_Insurance == 'Theft':
            acronym = 'TFT'
            class_id = '10'
        elif row.Class_Insurance == 'Workmen Compensation':
            acronym = 'WCA'
            class_id = '11'
        elif row.Class_Insurance == 'Medical':
            acronym = 'MDI'
            class_id = '12'
        elif row.Class_Insurance == 'Miscellaneous':
            acronym = 'MIS'
            class_id = '14'

        # Create a new insurance class
        new_insurance_class = InsuranceClass(
            class_id, row.Class_Insurance, acronym, row.Sector)
        new_insurance_class.save()


def insurance_subclass():
    # read file
    df = pd.read_csv("data/Classes_Insurance.csv")
    for row in df.itertuples():
        # get parent class
        parent_class = InsuranceClass.get_class_by_name(
            row.Class_Insurance)
        new_sub_class = InsuranceSubclass(
            row.Class_Code, row.Subclasses, parent_class)

        new_sub_class.save()

# Counties
def counties():
    df = pd.read_csv("data/County_Insurance.csv")
    for row in df.itertuples():
        new_county = County(row.County_Name)
        new_county.save()


def constituencies():
    df = pd.read_csv("data/Constituency_Insurance.csv")

    for row in df.itertuples():
        # TODO: Create get county by name
        county = County.get_county_by_name(row.County_Name)
        new_constituency = Constituency(row.Constituency_Name, county)
        new_constituency.save()


def ward():
    df = pd.read_csv("data/Ward_Insurance.csv")
    for row in df.itertuples():
        county_id = County.get_county_by_name(row.County_Name)
        constituency = Constituency.get_constituency_by_name(row.Constituency_Name)
        new_ward = Ward(row.Ward_Name, constituency, county_id)
        new_ward.save()


if __name__ == '__main__':
    car_makes()
    car_models()
    insurance_classes()
    insurance_subclass()
    counties()
    constituencies()
    ward()
