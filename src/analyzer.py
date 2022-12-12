import sklearn
import datetime
import pandas as pd

class TestSubject():

    def __init__(
        self,
        name : str,
        tested_from : datetime.datetime,
        tested_till : datetime.datetime
    ) -> None:
        self.name = name
        self.tested_from = tested_from
        self.tested_till = tested_till


class Analyzer():

    def __init__(
        self,
        test_subjects : list,
        raw_visit_result : pd.DataFrame,
        raw_sales_result : pd.DataFrame,
        raw_loc_result : pd.DataFrame,
        raw_face_result : pd.DataFrame
    
    ) -> None:
        self.test_subjects = test_subjects
        self.visit_results = self._split_result_according_to_test_subject(raw_test_results= raw_visit_result, data_column_name = raw_visit_result.columns(2))
        self.sales_results = self._split_result_according_to_test_subject(raw_test_results= raw_sales_result, data_column_name = raw_sales_result.columns(2))
        self.loc_results = self._split_result_according_to_test_subject(raw_test_results= raw_loc_result, data_column_name = raw_loc_result.columns(2))
        self.face_results = self._split_result_according_to_test_subject(raw_test_results= raw_face_result, data_column_name = raw_test_result.columns(2))


    def _split_result_according_to_test_subject(
        self,
        raw_test_results : pd.DataFrame,
        data_column_name :str
    ) -> list:

        test_results = []

        return test_results

    def test_hypothesis(self) -> dict:
        ## Using Baise method for A/B Testing

        ## 3 factors for testing :
        ##   1) Number of sales  
        ##   2) Period of time customer stayed at the item we are advertising
        ##   3) Number of People who looked our AD

        ## Expected Revenue Analysis
        ##   1) if People Saw the AD 

        reject = True

        return reject

    def _sale_analysis(self):

        ## A/B TESTING only according to sales
        visits = [1300, 1000]
        sales =  [80,50]
        

        
