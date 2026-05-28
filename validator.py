import pandas as pd
import re

def validate_data(df):

    report = {}

    # Missing values
    missing_values = df.isnull().sum()
    report["missing_values"] = missing_values.to_dict()

    # Duplicate rows
    duplicates = df.duplicated().sum()
    report["duplicate_rows"] = int(duplicates)

    # Invalid emails
    invalid_emails = []

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    for email in df["email"].dropna():

        if not re.match(email_pattern, email):
            invalid_emails.append(email)

    report["invalid_emails"] = invalid_emails

    # Invalid phone numbers
    invalid_phones = []

    for phone in df["phone"]:

        phone = str(phone)

        if len(phone) != 10:
            invalid_phones.append(phone)

    report["invalid_phones"] = invalid_phones

    # Suspicious salaries
    suspicious_salary = df[df["salary"] > 500000]

    report["suspicious_salary_count"] = len(suspicious_salary)

    return report