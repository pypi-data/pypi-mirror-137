# from plutus_backtest import backtest
# import numpy as np, numpy.random
# import random
# from datetime import datetime, timedelta
#
#
# list_assets = ["AAPL","AAPL", "ATVI", "AVNW", "HBIO", "F", "MS", "BAC"]
# # --------------------------------------------------------- #
# # START DATES GENERATION
# min_year=2017
# max_year=2017
#
# start = datetime(min_year, 1, 1, 00, 00, 00)
# years = max_year - min_year+1
# end = start + timedelta(days=365 * years)
#
# open_days = []
#
# for i in range(len(list_assets)):
#     random_date = start + (end - start) * random.random()
#     open_days.append(random_date.strftime("%Y-%m-%d"))
# # --------------------------------------------------------- #
# # --------------------------------------------------------- #
# # CLOSE DATES GENERATION
# min_year=2021
# max_year=2021
#
# start = datetime(min_year, 1, 1, 00, 00, 00)
# years = max_year - min_year+1
# end = start + timedelta(days=365 * years)
#
# close_days = []
#
# for i in range(len(list_assets)):
#     random_date = start + (end - start) * random.random()
#     close_days.append(random_date.strftime("%Y-%m-%d"))
# # --------------------------------------------------------- #
# # --------------------------------------------------------- #
# # WEIGHTS GENERATION (random numbers from 0 to 1 that sum to 1)
# weights = ((np.random.dirichlet(np.ones(len(list_assets)),size=1))*100).tolist()[0]
# # --------------------------------------------------------- #
#
# bt = backtest(asset = list_assets,
#               o_day = open_days,
#               c_day = close_days,
#               weights_factor = weights)
# bt.plotting()

from plutus_backtest import backtest

bt1 = backtest(asset = ["AAPL", "BTC-USD","GC=F"],
               o_day = ["2021-08-01", "2021-07-15", "2021-08-20"],
               c_day = ["2021-09-01", "2021-09-01","2021-09-15"])

bt2 = backtest(asset = ["AMZN", "EURUSD=X"],
               o_day = ["2021-06-01", "2021-06-15"],
               c_day = ["2021-06-30", "2021-07-05"])

p1 = bt1.portfolio_construction()
p2 = bt2.portfolio_construction()
q1 = bt1.final_portfolio
q2 = bt2.final_portfolio

dic ={}
dic[0] = q1
dic[1]= q2

combined_frame = backtest.puzzle_assembly(dic)

backtest.puzzle_execution(combined_frame)