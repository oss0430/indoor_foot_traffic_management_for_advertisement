import sklearn
import datetime
import pandas as pd
import numpy as np
import scipy

class TestSubject():

    def __init__(
        self,
        name : str,
        tested_from : datetime.datetime,
        tested_till : datetime.datetime,
        item_x : float,
        item_y : float
    ) -> None:
        self.name = name
        self.tested_from = tested_from
        self.tested_till = tested_till

        self.item_x = item_x
        self.item_y = item_y


class Analyzer():

    def __init__(
        self,
        test_subjects : list,

        raw_sales_result : pd.DataFrame,
        raw_loc_result : pd.DataFrame,
        raw_face_result : pd.DataFrame
    
    ) -> None:
        self.test_subjects = test_subjects
        
        ## List of PANDAS
        self.sales_results = self._split_result_according_to_test_subject(raw_test_results= raw_sales_result, date_column_name = raw_sales_result.columns(2))
        self.loc_results = self._split_result_according_to_test_subject(raw_test_results= raw_loc_result, date_column_name = raw_loc_result.columns(2))
        self.face_results = self._split_result_according_to_test_subject(raw_test_results= raw_face_result, date_column_name = raw_face_result.columns(2))
        
        ## DATA for Actual 
        self.time_spent  = self._from_loc_results_get_time_spent_results(self.loc_results)
        self.visit_count = self._from_loc_results_get_visit_results(self.loc_results)
        

    def _from_loc_results_get_visit_results(
        self,
        loc_results : list
    ) -> list:
        visit_count = []

        visit_count.append(len(loc_results[0]))
        visit_count.append(len(loc_results[1]))

        return visit_count


    def _from_loc_results_get_time_spent_results(
        self,
        loc_results : list
    ) -> list:

        ## Assuming every result has time window of 5 seconds

        def is_near(
            row : pd.Series,
            test_subject : TestSubject
        ):
            distance = np.sqrt((test_subject.item_x - row['x'])^2 + (test_subject.item_y - row['y'])^2)
            if distance < 2 :
                return True

            else :
                return False

        time_spent_results = []

        for index, loc_result in enumerate(loc_results):
            time_spent_result = {}
            for _, row in loc_result.iterrows():
                if is_near(row, self.test_subjects[index]) :
                    user_id = row['user_id']
                    if row['user_id'] in time_spent_result:
                        time_spent_result[user_id]["time_spent"] = time_spent_result[user_id]["time_spent"] + 5
                    else :
                        time_spent_result[user_id] = {
                            "time_spent" : 5
                        }
            time_spent_results.append(time_spent_result)

        ## USER | TIME_SPENT (NEAR_ITEM)
        ##   1  | 123
        ##   2  | 4331
        ##   4  | 543

        return time_spent_results


    def _split_result_according_to_test_subject(
        self,
        raw_test_results : pd.DataFrame,
        date_column_name :str
    ) -> list:

        test_results = []

        def distinguish_by_time(row):
            current_date = row[date_column_name]
            name = ""
            for test_subject in self.test_subjects:
                name = ""
                if current_date >= test_subject.tested_from and current_date <= test_subject.tested_till :
                    name =  test_subject.name
                    break
            
            return name

        raw_test_results['name'] = raw_test_results.apply(lambda x : distinguish_by_time(x), axis = 1)
        
        test_results.append(raw_test_results.loc[raw_test_results['name'] == self.test_subjects[0].name])
        test_results.append(raw_test_results.loc[raw_test_results['name'] == self.test_subjects[1].name])

        return test_results


    def do_reject_null_hypothesis(
        self,
        p_value : float,
        threshold : float = 0.05
    ) -> bool:

        if p_value < threshold:
            ## Reject the Null Hypothesis
            return True
        
        else :
            ## Failed to Reject the Null Hypothesis
            return False


    def _get_z_score(
        self,
        x : float,
        mean : float,
        std : float
    ) -> float:
        return (x- mean) /std


    def _z_score_two_distribution(
        self,
        n_control : int,
        n_variant : int,
        mean_control: float,
        mean_variant : float,
        var_control : float,
        var_variant : float
    ) -> float:
        s_mean = mean_variant - mean_control
        s_var = (var_control/n_control) + (var_variant/n_variant)

        z_score = s_mean / np.sqrt(s_var)

        return z_score


    def p_value_from_z(
        self,
        z_score : float
    ):
        p_value_1_tail = scipy.stats.st.norm(z_score)
        p_value_2_tail = p_value_1_tail * 2

        return p_value_2_tail


    def sale_analysis(self):

        distributions = []

        for idx, df_sales in enumerate(self.sales_results):
            distribution = {}
            distribution['n'] = len(self.visit_count[idx])
            sales_data = np.array(df_sales['count'].values.tolist())

            distribution['mean'] = float(np.mean(sales_data))
            distribution['var']  = float(np.var(sales_data))

            distributions.append(distribution)

        z_score = self._z_score_two_distribution(
            n_control= distributions[0]['n'],
            n_variant= distributions[1]['n'],
            mean_control= distributions[0]['mean'],
            mean_variant= distributions[1]['mean'],
            var_control = distributions[0]['var'],
            var_variant = distributions[1]['var']
        )

        p_value = self.p_value_from_z(z_score)

        return distributions, z_score, p_value

        
    def time_spent_analysis(self):
        
        distributions = []

        for idx, df_time_spent in enumerate(self.time_spent):
            distribution = {}
            distribution['n'] = len(self.visit_count[idx])
            time_spent_data = np.array(df_time_spent['time_spent'].values.tolist())

            distribution['mean'] = float(np.mean(time_spent_data))
            distribution['var']  = float(np.var(time_spent_data))

            distributions.append(distribution)

        z_score = self._z_score_two_distribution(
            n_control= distributions[0]['n'],
            n_variant= distributions[1]['n'],
            mean_control= distributions[0]['mean'],
            mean_variant= distributions[1]['mean'],
            var_control = distributions[0]['var'],
            var_variant = distributions[1]['var']
        )

        p_value = self.p_value_from_z(z_score)

        return distributions, z_score, p_value
    

    def face_count_analysis(self):

        distributions = []

        for idx, df_sales in enumerate(self.sales_results):
            distribution = {}
            distribution['n'] = len(self.visit_count[idx])
            sales_data = np.array(df_sales['count'].values.tolist())

            distribution['mean'] = float(np.mean(sales_data))
            distribution['var']  = float(np.var(sales_data))

            distributions.append(distribution)

        z_score = self._z_score_two_distribution(
            n_control= distributions[0]['n'],
            n_variant= distributions[1]['n'],
            mean_control= distributions[0]['mean'],
            mean_variant= distributions[1]['mean'],
            var_control = distributions[0]['var'],
            var_variant = distributions[1]['var']
        )

        p_value = self.p_value_from_z(z_score)

        return distributions, z_score, p_value

            

        
        
