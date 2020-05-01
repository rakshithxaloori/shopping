import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Read data from file
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        data = []
        for row in reader:
            administrative = int(row[0])
            administrative_duration = float(row[1])
            informational = int(row[2])
            product_related = int(row[3])
            product_related_duration = float(row[4])
            bounce_rates = float(row[5])
            exit_rates = float(row[6])
            page_values = float(row[7])
            special_day = float(row[8])

            switcher = {
                "Jan": 0,
                "Feb": 1,
                "Mar": 2,
                "Apr": 3,
                "May": 4,
                "Jun": 5,
                "Jul": 6,
                "Aug": 7,
                "Sep": 8,
                "Oct": 9,
                "Nov": 10,
                "Dec": 11,
            }

            month = switcher.get(row[9], None)
            if month is None:
                raise ValueError

            operating_systems = int(row[10])
            browser = int(row[11])
            region = int(row[12])
            traffic_type = int(row[13])

            if row[14] == "New_Visitor":
                visitor_type = 0
            else:
                visitor_type = 1

            if row[15] == "FALSE":
                weekend = 0
            else:
                weekend = 1

            if row[16] == "FALSE":
                purchased = 0
            else:
                purchased = 1

            data.append({
                "evidence": [administrative, administrative_duration, informational, product_related, product_related_duration, bounce_rates, exit_rates, page_values, special_day, month, operating_systems, browser, region, traffic_type, visitor_type, weekend],
                "label": purchased
            })

    # Seperate data into evidence and labels lists
    evidence = [row["evidence"] for row in data]
    labels = [row["label"] for row in data]

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)

    # Fit model
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positive_labels_count = 0
    negative_labels_count = 0
    for label, prediction in zip(labels, predictions):
        if label = 0:
            # true_positive_rate
            if label == prediction:
                positive_labels_count += 1
        elif label == 1:
            # true_negative_rate
            if label == prediction:
                negative_labels_count += 1

    total_labels_count = len(labels)

    sensitivity = float(positive_labels_count)/float(total_labels_count)
    specificity = float(negative_labels_count)/float(total_labels_count)
    
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
