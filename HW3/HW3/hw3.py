from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    """This function will load the data from the file center it around the 
        center and return it as an array of floats"""

    # parameters: filename              

    x = np.load(filename)
    return x - np.mean(x, axis = 0)


def get_covariance(dataset):
    """This method will calculate and return the covariance matrix of the dataset as a numpy
        matrix (d × d array). """

    # Parameter: dataset
    
    return np.dot(np.transpose(dataset), dataset)

def get_eig(S, m):
    """This method will perform eigendecomposition on the covariance matrix S and return a diagonal matrix
        (numpy array) with the largest m eigenvalues on the diagonal in descending order, and a matrix (numpy
        array) with the corresponding eigenvectors as columns."""

    # Parameter: S(covariance matrix)
    # Patameter: m(number of eigenvalues)
    eigenvalues, eigenvectors = eigh(S, subset_by_index=[len(S)-m,len(S)-1])
    idx = np.argsort(eigenvalues)
    idx = idx[::-1]
    eigenvectors = eigenvectors[:, idx]
    eigenvalues = eigenvalues[idx]
    return np.diag(eigenvalues), eigenvectors

def get_eig_prop(S, prop):
    """This method is used to extract eigenvalues and eigenvectors"""
    eigenvalues, eigenvectors = eigh(S, subset_by_value=[len(S)-prop,len(S)-1])
    idx = np.argsort(eigenvalues)
    idx = idx[::-1]
    eigenvectors = eigenvectors[:, idx]
    eigenvalues = eigenvalues[idx]
    return np.diag(eigenvalues), eigenvectors

def project_image(image, U):
    # This method will return the projection of the given image
    score = np.dot(np.transpose(U), image)
    projection = np.dot(U, score) * np.transpose(np.mean(image, axis = 0))
    projection = np.reshape(projection, (32,32))
    
    return projection

def display_image(orig, proj):
    # This method will create the 2 subplots of original and projected image

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_title("Original")
    ax2.set_title("Projection")
    a = ax1.imshow(np.transpose(np.reshape(orig,(32,32))), aspect='equal')
    c = ax2.imshow(np.transpose(proj), aspect='equal')
    plt.show()
