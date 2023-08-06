import os
import pandas as pd
from rltrade import config
from rltrade.data import load_csv
from rltrade.backtests import get_metrics
from rltrade.models import SmartPortfolioLearnerAgent,SmartPortfolioMainAgent

demo = True
time_frame = '1 day'
trade_period = ('2021-12-29','2022-02-01') #yesterday's date
accountid = "DU1770002"


csv_path = 'testdata/ibkr1day.csv'
path = 'models/learner'

tech_indicators = [
    "open_2_sma",
    "close_2_tema",
    "tema"
]

additional_indicators = [
    "max_value_price_5",
    "max_value_price_22",
    "max_value_price_66",
    "max_value_price_1year",
    "max_value_price_3year",
    "max_value_price_5year",
    "min_value_price_5",
]

all_indicators = tech_indicators + additional_indicators

df_actions = pd.DataFrame()
for i,indicator in enumerate(all_indicators):

    PPO_PARAMS = {'ent_coef':0.005,
                'learning_rate':0.01,
                'batch_size':252}

    df = load_csv(csv_path) # run download script before this

    print(f"Iteration: {i}")
    save_path = path+"/"+str(i)
    tech_indicator = [indicator] if indicator in tech_indicators else []
    additional_indicator = [indicator] if indicator in additional_indicators else []

    print(tech_indicator,additional_indicator)

    env_kwargs = {
    "initial_amount": 50_828, 
    "ticker_col_name":"tic",
    "transaction_cost":1.5,
    "target_metrics":['asset','sortino','calamar','skew','kurtosis'], #asset, cagr, sortino, calamar, skew and kurtosis are available options.
    "tech_indicator_list":tech_indicator + additional_indicator, 
    "reward_scaling": 1}

    agent = SmartPortfolioLearnerAgent("ppo",
                    df=None,
                    ticker_list=None,
                    train_period=None,
                    test_period=None,
                    sec_types=None,
                    exchanges=None,
                    ticker_col_name="tic",
                    tech_indicators=tech_indicator,
                    additional_indicators=additional_indicator,
                    env_kwargs=env_kwargs,
                    model_kwargs=PPO_PARAMS,
                    tb_log_name='ppo',
                    time_frame=time_frame,
                    demo=demo,
                    epochs=1)

    agent.load_model(save_path)
    temp = agent.get_trade_actions(path,trade_period)
    df_actions = df_actions.append(temp)

    if (i+1) == len(all_indicators):
        os.remove(path+"/data.csv")


df_actions['date'] = pd.to_datetime(df_actions['date'])

MAIN_PPO_PARAMS = {'ent_coef':0.005,
            'learning_rate':0.01,
            'batch_size':252}

main_env_kwargs = {
    "initial_amount": 50_828, 
    "ticker_col_name":"tic",
    "transaction_cost":1.5,
    "filter_threshold":0.25, #between 0.1 to 1, select percentage of top stocks 0.3 means 30% of top stocks
    "target_metrics":['asset','sortino','calamar','skew','kurtosis'], #asset, cagr, sortino, calamar, skew and kurtosis are available options.
    "reward_scaling": 1}

agent = SmartPortfolioMainAgent("ppo",
                    df=None,
                    ticker_list=None,
                    sec_types=None,
                    exchanges=None,
                    train_period=None,
                    test_period=None,
                    ticker_col_name="tic",
                    env_kwargs=main_env_kwargs,
                    model_kwargs=MAIN_PPO_PARAMS,
                    tb_log_name='ppo',
                    time_frame=time_frame,
                    demo=demo,
                    epochs=10)

agent.load_model(path+'/main')
actions = agent.get_trade_actions(df_actions,trade_period)
agent.make_trade(actions,accountid)

