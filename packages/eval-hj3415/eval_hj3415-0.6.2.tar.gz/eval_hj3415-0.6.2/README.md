eval-hj3415
==========

eval-hj3415 evaluate naver financial data.


Quick start
------------

from eval_hj3415 import eval

for all eval dictionary..
   eval.Eval(<<code:str>>).get_all()
or..
   eval.Score(<<code:str>>).eval_dict

for get score..
   s = eval.Score(<<code:str>>)
   s.red()
   s.mil()
   s.blue()