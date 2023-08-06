from rltrade.backtests import plot_chart_forex, plot_chart_stocks

#for forex
# path = 'models/daytrades/forex-train11-single-2'
# symbol = 'GOLD'
# lot_size = 0.01
# plot_chart_forex(path,symbol,lot_size)

# for stocks
path = 'models/learner/main'
symbol = 'pall'
plot_chart_stocks(path,symbol)