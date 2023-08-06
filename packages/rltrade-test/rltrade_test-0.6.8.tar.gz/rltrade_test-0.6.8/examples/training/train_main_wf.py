import pandas as pd
from rltrade import config
from rltrade.data import load_csv
from rltrade.backtests import get_metrics
from rltrade.models import SmartPortfolioLearnerAgent,SmartPortfolioMainAgent

demo = True
time_frame = '1 day'
train_period = ('2012-01-01','2020-01-01') #for training the model
test_period = ('2020-01-02','2021-12-29') #for trading and backtesting

csv_path = 'testdata/ibkr1day.csv'
path = 'models/learner_cv'

ticker_list = ['pall', 'rio', 'spy', 'tlt', 'jbss', 'aapl']
sec_types = ['STK'] * len(ticker_list)
exchanges = ['SMART'] * len(ticker_list)
# tech_indicators = config.STOCK_INDICATORS_LIST
# additional_indicators = config.ADDITIONAL_STOCK_INDICATORS

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


for i,indicator in enumerate(all_indicators):

    PPO_PARAMS = {'ent_coef':0.005,
                'learning_rate':0.01,
                'batch_size':252}

    df = load_csv(csv_path) # run download script before this
    # df = df[df['tic'].isin(ticker_list)].reset_index(drop=True)

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
                        df=df,
                        ticker_list=ticker_list,
                        sec_types=sec_types,
                        exchanges=exchanges,
                        ticker_col_name="tic",
                        tech_indicators=tech_indicator,
                        additional_indicators=additional_indicator,
                        train_period=train_period,
                        test_period=test_period,
                        env_kwargs=env_kwargs,
                        model_kwargs=PPO_PARAMS,
                        tb_log_name='ppo',
                        time_frame=time_frame,
                        demo=demo,
                        epochs=2)

    agent.train_model()
    agent.make_prediction() #testing model on testing period
    agent.save_model(save_path) #save the model for trading

##############
# Main model #
##############
df_actions = pd.DataFrame()
for i in range(len(all_indicators)):
    load_path = path + "/" + str(i)
    df = pd.read_csv(load_path+'/action_df.csv')
    df_actions = df_actions.append(df)
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

start = df_actions['date'].min()
end = df_actions['date'].max()
date_range = pd.date_range(start=start,end=end,freq='1 Y') 

if test_period[1] not in date_range:
    date_range = [x.strftime('%Y-%m-%d') for x in date_range] + [test_period[1]]
print(date_range)

for i in range(len(date_range)-2):

    train_period_ = (date_range[0],date_range[i+1])
    test_period_ = (date_range[i+1],date_range[i+2])

    print("Train Period: ",train_period_)
    print("Test Period: ",test_period_)

    agent = SmartPortfolioMainAgent("ppo",
                        df=df_actions,
                        ticker_list=ticker_list,
                        sec_types=sec_types,
                        exchanges=exchanges,
                        ticker_col_name="tic",
                        train_period=train_period_,
                        test_period=test_period_,
                        env_kwargs=main_env_kwargs,
                        model_kwargs=MAIN_PPO_PARAMS,
                        tb_log_name='ppo',
                        time_frame=time_frame,
                        demo=demo,
                        epochs=10)

    agent.train_model()
    agent.make_prediction() #testing model on testing period
    agent.train_model_filter()
    agent.save_model(path+f"/main{i}") #save the model for trading

agent.save_model(path+"/main") #save the model for trading

for i in range(len(date_range)-2):

    train_period_ = (date_range[0],date_range[i+1])
    test_period_ = (date_range[i+1],date_range[i+2])

    print("Train Period: ",train_period_)
    print("Test Period: ",test_period_)

    get_metrics(path+f"/main{i}")