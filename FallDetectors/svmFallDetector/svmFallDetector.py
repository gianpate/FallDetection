import pandas as pd
from sklearn.svm import SVC 
from sklearn.model_selection import train_test_split  

def trainSVM(data:str) -> SVC:
    df = pd.read_csv(data)

    print("First 5 rows:")
    print(df.head())

    x = df.drop(columns=['sample_name', 'expected'])  # recognizer columns
    y = df['expected']                                # target labels

    print(f"Feature shape: {x.shape}")   # (60, 8)
    print(f"Target shape: {y.shape}")    # (60,)


    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.07, stratify=y, random_state=42)

    #  initialize SVM
    svm = SVC()

    # Train 
    svm.fit(x_train, y_train)

    accuracy = svm.score(x_test, y_test)
    print(f"Test accuracy: {accuracy:.2f}")

    return svm






