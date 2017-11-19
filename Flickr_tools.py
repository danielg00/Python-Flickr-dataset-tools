from os import listdir
import pandas as pd
from tqdm import tqdm


class Flickr8kAPI:

    def __init__(self, path_to_tokens, path_to_imgs):
        self._path_to_tokens = path_to_tokens
        self._path_to_imgs = path_to_imgs

    def _load(self):
        data = pd.read_csv(
            self._path_to_tokens,
            sep='\t', header=None,
            index_col=None)

        return data[0], data[1]

    def _compress_imgList(self, ims):
        start = 0
        im_c = []
        for i in ims:
            if i[-1] == '2':
                line = i[:i.index('jpg')+3]
                im_c.append(line)
        return im_c

    def _sentences_to_lists(self, sent_list):
        ls = []
        start = 0
        print("Grouping sentences into lists of 5...")
        for _ in tqdm(sent_list):
            ls.append(list(sent_list[start:start+5]))
            start += 5
        return ls

    def tokens_to_dict(self):
        """
        Returns dict in the form:
        'image_name': ['sentence1', 'sentence2'...etc]
        """
        ims, snts = self._load()
        ims = self._compress_imgList(ims)
        snts = self._sentences_to_lists(snts)
        self.tokens2dict = dict(zip(ims, snts))

    def check_img_exists(self):
        """
        Checks if all images for dict are existant in directory
        """
        jpgs = listdir(self._path_to_imgs)
        dont_exist = []
        for i in tqdm(self.tokens2dict):
            if i not in jpgs:
                x = input("Cannot find image {0} , Remove? (y/n): ".format(i))
                if x == 'y':
                    dont_exist.append(i)

        for i in dont_exist:
            del self.tokens2dict[i]

    def get_dict(self):
        return self.tokens2dict

    def save_senteces(self, fname):
        """
        Saved to csv file. Use pandas.read_csv() to read safely
        """
        s = list(self.tokens2dict.values())
        pd.DataFrame(s).to_csv((fname+'.csv'))

    def save_images(self, fname):
        tks = self.tokens2dict
        im = list(tks.keys())
        pd.DataFrame(im).to_csv((fname + '.csv'))
