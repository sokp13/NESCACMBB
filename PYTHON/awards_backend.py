import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import pickle

class MVPModel:
    def __init__(self):
        self.model = None

    def train_model(self, X_train, y_train):
        self.model = DecisionTreeClassifier(random_state=42)
        self.model.fit(X_train, y_train)

    def save_model(self):
        with open('mvp_model.pkl', 'wb') as model_file:
            pickle.dump(self.model, model_file)

# Load your dataset
df = pd.read_csv('csv/MVP.csv')

# Assuming 'MVP' is the column indicating whether a player won MVP or not
le = LabelEncoder()
df['MVP'] = le.fit_transform(df['MVP'])

# Selecting features (PER, ORtg, basic five stats, team conference record)
features = ['PER', 'oRtg', 'pts', 'reb', 'stl', 'blk', 'nescac_wins']

# Extracting features and target variable
X = df[features]
y = df['MVP']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create an instance of MVPModel
mvp_model_instance = MVPModel()

# Train the model
mvp_model_instance.train_model(X_train, y_train)

# Save the trained model
mvp_model_instance.save_model()



# # Make predictions on the test set
# predictions = mvp_model_instance.model.predict(X_test)

# # Evaluate the model
# accuracy = accuracy_score(y_test, predictions)
# print(f'Accuracy: {accuracy:.2f}')

# # Print classification report
# print('\nClassification Report:')
# print(classification_report(y_test, predictions))
