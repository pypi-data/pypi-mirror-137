import sklearn.metrics
import csv
from operator import itemgetter
import scipy.stats
import sys
import numpy as np

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn






def print_test():
    print("test!!!!")




def read_csv(filename):
    # for CSVs with format, no header:
    # Gene1, 1.4, 3.2, 4.5
    # Gene2, 2.2, 3.2, 1.1


    # returns data in [genes, samples] shape

    genes = []
    data = []

    with open(filename) as csvfile:

        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            genes.append(row[0])
            data.append(row[1:])


    data = data[1:]
    genes = genes[1:]
    data = np.array(data).astype(float)


    return(genes,data)





def write_phixer_input(data,filename):

    # takes data in [genes, samples] shape

    # writes .txt file

    with open(filename, "w") as record_file:

        for row in range(data.shape[0]):

            for col in range(data.shape[1]-1):
                record_file.write(str(data[row,col])+",")

            record_file.write(str(data[row,data.shape[1]-1]))

            record_file.write("\n")






def process_raw_phixer(genes,data,file_in="", file_out="output.txt"):
    # takes raw phixer network as input
    # creates cytoscape net file as output
    edges_in = []
    with open(file_in) as tsvfile:

        spamreader = csv.reader(tsvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            edges_in.append([int(row[0]), int(row[1]), float(row[2]) ])



    N = len(genes)


    edges = np.zeros(shape=(N,N))

    for row in edges_in:
        if row[0] != row[1]:
            edges[row[0]-1,row[1]-1] = row[2]

    to_write = []

    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i,j] != 0:
                if np.cov(data[i,:],data[j,:])[0,1] > 0:
                    to_write.append([genes[i],genes[j],edges[i,j],1])
                else:
                    to_write.append([genes[i],genes[j],edges[i,j],-1])




    to_write = sorted(to_write, key=itemgetter(2), reverse=True)


    f = open(file_out, "w")
    f.write("source_node\tedge_sign\ttarget_node\tweight\n")
    for row in to_write:
        if int(row[3])==1:
            f.write("%s\tpositive\t%s\t%s\n" % (row[0],row[1],row[2]))
        else:
            f.write("%s\tnegative\t%s\t%s\n" % (row[0],row[1],row[2]))
    f.close()









def correlation(data, get_p_value=False ):

    edges = np.zeros(shape=(data.shape[0],data.shape[0]))

    # correlation
    for i in range(data.shape[0]):
        for j in range(i+1,data.shape[0]):
            cor, p_value = scipy.stats.pearsonr(data[i,:],data[j,:])
            # dot product in numerator, euclidian norm in denomenator

            if get_p_value:
                edges[i,j] = p_value
                edges[j,i] = p_value
            else:
                edges[i,j] = cor
                edges[j,i] = cor
    return(edges)
