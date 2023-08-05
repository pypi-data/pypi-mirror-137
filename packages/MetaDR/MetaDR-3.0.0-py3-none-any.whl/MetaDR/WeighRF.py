import argparse as ap
import pandas as pd
import numpy as np
import sys
from sklearn import preprocessing
import argparse as ap
import pandas as pd
import numpy as np
import sys
import os
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import time
import os
from scipy import stats
from numpy.random import seed
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel




def train(data,test_split, repeat_times):  # python3 WRF_EV.py --fn Karlsson_T2D --rs 2 --ts 0.3
    # print("333")

    def read_params(args):
        parser = ap.ArgumentParser(description='Specify the probability')
        arg = parser.add_argument
        arg('-fn', '--fn', type=str, help='datasets')
        # arg('-ns', '--ns', type=str, help='number of select biomarkers')
        arg('-ts', '--ts', type=str, help='the ratio of test data')
        arg('-rs', '--rs', type=str, help='repeat times')

        return vars(parser.parse_args())


    def read_files(data):


        # file_name='Karlsson_T2D'

        known = pd.read_csv( data+'_known.csv', index_col=0)
        unknown = pd.read_csv( data+'_unknown.csv', index_col=0)

        y = pd.read_csv( data+'_y.csv', index_col=0)
        le = preprocessing.LabelEncoder()
        y = np.array(y).ravel()
        y = le.fit_transform(y)
        return known, unknown, y



    def WRF_eva(known, unknown,y, test_split, repeat_times, data ):
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import f1_score
        from sklearn.metrics import roc_auc_score
        import time
        import os
        from scipy import stats
        from numpy.random import seed
        from sklearn.model_selection import RandomizedSearchCV
        from sklearn.ensemble import RandomForestClassifier

        start = time.time()

        known_X = np.array(known)
        unknown_X = np.array(unknown)

        knownX_train, knownX_test, unknownX_train, unknownX_test, y_train, y_test = train_test_split(
            known_X, unknown_X, y, test_size=test_split, random_state=4489)

        ave_auc = []
        repeat_seed = repeat_times

        path =  data+'_WRF_ev.txt'
        if os.path.exists(path):
            os.remove(path)
        file = open(path, 'a')



        feature_imp = []

        kweight = []

        for i in range(repeat_seed):

            print('Round ' + str(i + 1))

            seed(i)
            y_predpro = []


            paramsampler = {'max_features': stats.uniform(0, 1.0),
                            'max_depth': stats.randint(1, 10), "n_estimators": stats.randint(100, 2000)}

            clf = RandomizedSearchCV(
                RandomForestClassifier(oob_score=True),
                param_distributions=paramsampler,
                cv=5, n_jobs=-1)

            clf.fit(knownX_train, y_train)

            clfz = RandomizedSearchCV(
                RandomForestClassifier(oob_score=True),
                param_distributions=paramsampler,
                cv=5, n_jobs=-1)

            clfz.fit(unknownX_train, y_train)

            known_oob = clf.best_score_
            unknown_oob = clfz.best_score_

            known_weight = known_oob / (known_oob + unknown_oob)

            unknown_weight = 1 - known_weight

            kweight.append(known_weight)

            print('known weight:  %.4f' % known_weight, 'unknown weight: %.4f' % unknown_weight)






            combinedX_train = np.hstack((known_weight * knownX_train, unknown_weight * unknownX_train))

            combinedX_test = np.hstack((known_weight * knownX_test, unknown_weight * unknownX_test))

            clfc = RandomizedSearchCV(
                RandomForestClassifier(),
                param_distributions=paramsampler,
                cv=5, n_jobs=-1)

            clfc.fit(combinedX_train, y_train)

            importances = clfc.best_estimator_.feature_importances_

            feature_imp.append(importances)

            pred_prob = clfc.predict_proba(combinedX_test)[:, 1]

            y_predpro.extend(pred_prob)

            auc = roc_auc_score(y_test, pred_prob)

            ave_auc.append(auc)

            print('AUC :  %.4f' % auc)

        print('Mean AUC :  %.4f' % np.mean(ave_auc))
        print('Ave Known Weight :  %.4f' % np.mean(kweight))
        print('Ave unKnown Weight :  %.4f' % (1 - np.mean(kweight)))

        end = time.time()
        running_time = end - start
        print('Time cost : %.5f s' % running_time)


        meanauc=np.mean(ave_auc)
        mkweight=np.mean(kweight)
        mukweight=1 - np.mean(kweight)
        print('====================')
        file.write('Mean AUCs: ' + str(meanauc) + "\n")
        file.write('Mean Known weights: ' + str(mkweight) + "\n")
        file.write('Mean Unknown weights: ' + str(mukweight) + "\n")

        file.write('Time for '+str(repeat_seed)+' rounds running: ' + str(running_time) + "s")


        return clfc, mkweight, mukweight, meanauc

    # par = read_params(sys.argv)

    # file_name = str(par['fn'])
    # ts = float(par['ts'])
    # rs = int(par['rs'])

    known, unknown,y=read_files(data)
    clfc, mkweight, mukweight, meanauc = WRF_eva(known, unknown,y, test_split, repeat_times, data )

    return clfc, mkweight, mukweight, meanauc


def select(data, select_nums, repeat_times):  # python3 WRF_FS.py --fn Karlsson_T2D --rs 2 --tp 30
    def read_params(args):
        parser = ap.ArgumentParser(description='Specify the probability')
        arg = parser.add_argument
        arg('-fn', '--fn', type=str, help='datasets')

        arg('-tp', '--tp', type=str, help='number of select features')

        arg('-rs', '--rs', type=str, help='repeat times')

        return vars(parser.parse_args())


    def read_files(data):


        # file_name='Karlsson_T2D'

        known = pd.read_csv(data+'_known.csv', index_col=0)
        unknown = pd.read_csv(data+'_unknown.csv', index_col=0)

        y = pd.read_csv(data+'_y.csv', index_col=0)
        le = preprocessing.LabelEncoder()

        y=np.array(y).ravel()
        y = le.fit_transform(y)
        return known, unknown, y


    def WRF_sff(known, unknown, y):


        known_X = np.array(known)
        unknown_X = np.array(unknown)

        paramsampler = {'max_features': stats.uniform(0, 1.0),
                        'max_depth': stats.randint(1, 10), "n_estimators": stats.randint(100, 2000)}

        clfx = RandomizedSearchCV(
            RandomForestClassifier(random_state=4487),
            param_distributions=paramsampler,
            cv=5, n_jobs=-1, random_state=4489)

        clfx.fit(known_X, y)

        clfz = RandomizedSearchCV(
            RandomForestClassifier(random_state=4487),
            param_distributions=paramsampler,
            cv=5, n_jobs=-1, random_state=4489)

        clfz.fit(unknown_X, y)

        known_oob = clfx.best_score_
        unknown_oob = clfz.best_score_

        known_weight = known_oob / (known_oob + unknown_oob)

        unknown_weight = 1 - known_weight

        combinedX = np.hstack((known_weight * known_X, unknown_weight * unknown_X))

        paramsampler = {'max_features': stats.uniform(0, 1.0),
                        'max_depth': stats.randint(1, 10), "n_estimators": stats.randint(100, 2000)}
        clfc = RandomizedSearchCV(
            RandomForestClassifier(random_state=4487),
            param_distributions=paramsampler,
            cv=5, n_jobs=-1, random_state=4489)

        clfc.fit(combinedX, y)

        rf = clfc.best_estimator_

        model = SelectFromModel(rf, prefit=True)

        slf = model.get_support()
        slf = list(slf)
        slf=[int(i) for i in slf]
        return known_weight, unknown_weight, slf





    # par = read_params(sys.argv)

    # file_name = str(par['fn'])
    # tp = int(par['tp'])
    # rs = int(par['rs'])



    known, unknown,y=read_files(data)

    raw_fea = known.columns.values.tolist()
    un_fea = unknown.columns.values.tolist()
    feature_lab = raw_fea + un_fea
    print('all_feature_length: ' + str(len(feature_lab)))



    all_score=[]
    for i in range(repeat_times):
        seed(i)
        top30_rawfeature=WRF_sff(known, unknown,y)
        all_score.append(top30_rawfeature[2])

    all_score=np.array(all_score).reshape(repeat_times,-1)

    ave_importances=np.mean(all_score, axis=0)

    sfn=[i for i in ave_importances if i!=0]

    indices = np.argsort(ave_importances)[::-1]


    weighted_features=[]
    for f in range(select_nums):
        weighted_features.append(feature_lab[indices[f]])

    print('Selected features: ' + str(len(sfn)))
    print('Top '+str(select_nums)+' features: ' + "\n"+ str(weighted_features))

    path =  data + '_WRF_fs.txt'
    if os.path.exists(path):
        os.remove(path)
    file = open(path, 'a')

    file.write('Selected features: ' + str(len(sfn))+ "\n")
    file.write('Top '+str(select_nums)+' features: ' + "\n"+ str(weighted_features))

    return weighted_features



# ens_model, known_weight, unknown_weight, ens_auc = train(data='data/Karlsson_T2D',test_split=0.3, repeat_times=1)  # python3 WRF_EV.py --fn Karlsson_T2D --rs 2 --ts 0.3

# top_features = select(data='data/Karlsson_T2D', select_nums=30, repeat_times=1)  # python3 WRF_FS.py --fn Karlsson_T2D --rs 2 --tp 30
