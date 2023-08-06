from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_confusion_matrix(y_true, y_pred, ax=None, title='Confusion Matrix', xlabel='Predicted', ylabel='True'):
    '''
    Plots a confusion matrix for given true and predicted labels.

            Parameters:
                    y_true: An (n,) array of ground truth labels (boolean, categorical)
                    y_pred: An (n,) array of predicted labels (boolean, categorical)
                    ax: A pyplot axes object
                    title (str): The plot title
                    xlabel (str): The X label
                    ylabel (str): The Y label
    '''

    if ax == None:
        fig, ax = plt.subplots()

    labels = np.unique(y_true)

    cm = confusion_matrix(y_true, y_pred)

    df_cm = pd.DataFrame(cm, labels, labels)

    sns.heatmap(df_cm, cmap='Blues', cbar=False, annot=True, ax=ax)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)


if __name__=='__main__':

    y_true = [False, True, True, False, False, True, True, False]
    y_pred = [False, True, True, False, False, True, False, False]

    plot_confusion_matrix(y_true, y_pred)
    plt.show()