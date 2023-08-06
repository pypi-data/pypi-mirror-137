from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_confusion_matrix(y_true, y_pred, ax=None):

    if ax == None:
        fig, ax = plt.subplots()

    labels = np.unique(y_true)

    cm = confusion_matrix(y_true, y_pred)

    df_cm = pd.DataFrame(cm, labels, labels)

    sns.heatmap(df_cm, cmap='Blues', annot=True, ax=ax)

    ax.set_title("Confusion Matrix")
