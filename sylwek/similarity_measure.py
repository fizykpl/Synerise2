from multiprocessing.pool import ThreadPool

from sklearn import metrics

class SimilarityMeasure:
    cache = {}
    images = {}
    MI = "MI"
    pool = ThreadPool(8)

    def __init__(self,images):
        self.images = images
        #  Add cache for Mutual Information
        self.cache[self.MI] = {}

    def most_similar(self, source_id, top_limit):
        """
        4. Prosimy przygotować funkcję pozwalającą na znalezienie K (K z zakresu <1;50>) identyfikatorów obrazków o wektorach najbardziej podobnych (dowolna miara podobieństwa, może być euclidesowa) do zadanego przez identyfikator,
        :param source_id:  image id
        :param top_limit:  limit most similar
        :return:
        """

        if not source_id in self.cache[self.MI]:
            print('Calculate MI score for id = %s.' % source_id)
            #  Calculate MI score
            measurement = self.calculate_score_MI(source_id)
            # Calculate top
            top = self.calculate_top(measurement,source_id)
            self.cache['MI'][source_id] = top
        else:
            print('Get from cache MI score for id = %s.' % source_id)
            top = self.cache['MI'][source_id]

        top = top[1:]  # Omit index 0 is score for 'source_id'
        output = [t[1] for t in top[:top_limit]]
        return output

    def calculate_top(self, score,id):
        top = [[score[id], id] for id in self.images]
        top = sorted(top, key=lambda x: x[0], reverse=True)
        top = top[0:51]  # on index 0 is score for 'source_id'
        return top

    def calculate_score_MI(self, source_id):
        parameters = [(source_id, image_id,) for image_id in self.images]
        parameters = tuple(parameters)
        score_MI = self.pool.map(self._mutual_infomation_helper, parameters)
        return score_MI

    def _mutual_infomation(self,source_id, pred_id):
        mi =  metrics.mutual_info_score(self.images[source_id], self.images[pred_id])
        return mi



