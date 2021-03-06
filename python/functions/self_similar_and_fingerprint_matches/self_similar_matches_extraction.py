## Import libraries
import numpy as np

ALPHA=0.05 # this constant allow us to determine the quantiles to be used to discriminate self-similar matches

## This function discriminates between normal matches and self-similar matches,
## i.e. matches that could be legitimately ambiguous (this matches could not pass the ratio test).
## This happens because the template itself has many similar parts
def self_similar_matches_extraction(matches,second_matches,template_descriptors):
    
    ## Creation of an array of all the distances between each feature and its second match
    distances = np.zeros(len(second_matches))
    for i,match in enumerate(second_matches):
        template_descriptor1 = np.float32(template_descriptors[match.trainIdx])
        template_descriptor2 = np.float32(template_descriptors[match.queryIdx])
        distances[i]=np.linalg.norm(template_descriptor1-template_descriptor2)
    ## Define the quantiles used to discriminate self-similar matches
    self_similar_quantile = np.percentile(distances, ALPHA*100)
    
    ## Compute the list that contains, for each template feature, its matches that not pass the quantile test.
    ## This means that this matches could be considered self-similar
    self_similar_list=[[] for i in range(len(matches))]
    
    search_for_more_neighbors = False # if at least one of the features has k self-similar matches, more neighbors has to be computed to find other possible self-simlar matches
    for i,kmatches in enumerate(matches):
        j=0
        no_more_selfs = False # if true, no more self-simlar matches possible for the current feature, and so the search stops
        while j<len(kmatches) and no_more_selfs==False:
            ## Extract the SIFT descriptor for the current feature and its actual considered match
            template_descriptor1 = np.float32(template_descriptors[kmatches[j].trainIdx])
            template_descriptor2 = np.float32(template_descriptors[kmatches[j].queryIdx])
            
            ## Compute the distance between the descriptors using the Euclidean norm
            distance = np.linalg.norm(template_descriptor1-template_descriptor2)
            
            ## Quantile test executed only on the left tail, since in a self-similar
            ## match the features are similar
            if distance<self_similar_quantile:
                self_similar_list[i].append(kmatches[j])
                if j==len(kmatches)-1:
                    search_for_more_neighbors=True
            else:
                no_more_selfs= True
            j+=1
            
    return self_similar_list, search_for_more_neighbors, self_similar_quantile