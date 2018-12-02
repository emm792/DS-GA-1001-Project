import itertools
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, log_loss
import numpy as np
import pandas as pd

'''
Collection of functions for metric reporting.
'''


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    
    Args:
        cm (array): Confusion matrix to be plotted.
        normalize (bool): If true, normalize the confusion matrix.
        title (str): Plot title.
        cmap: Matplotlib colormap.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        #print("Normalized confusion matrix")
    else:
        pass
       # print('Confusion matrix, without normalization')

    #print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    #plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    
    
def calc_performance(y_true, y_pred, y_pred_proba):
    cross_ent = log_loss(y_true, y_pred_proba)
    accuracy = accuracy_score(y_true, y_pred)
    result_list = [cross_ent, accuracy]
    indices = ['cross_entropy', 'accuracy']
    results = pd.DataFrame(result_list, index=indices, columns=['Score'])
    return results


def calc_test_train_performance(estimator, x_train, x_test, y_train, y_test, binary=False):
    y_pred_train = estimator.predict(x_train)
    y_pred_test = estimator.predict(x_test)
    y_proba_train = estimator.predict_proba(x_train)
    y_proba_test = estimator.predict_proba(x_test)
    if binary:
        y_proba_train = y_proba_train[:,1]
        y_proba_test = y_proba_test[:,1]
        
    train_perf = calc_performance(y_train, y_pred_train, y_proba_train)
    test_perf = calc_performance(y_test, y_pred_test, y_proba_test)
    
    # Should rename this to all_perf or something for clarity.... oh well
    train_perf.columns = ['Train_Score']
    train_perf['Test_Score'] = test_perf['Score']
    
    # Train perf now contains both train and test performance
    return train_perf


