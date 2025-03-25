from log_parser import Parser
parser = Parser("./backtests/2025-03-25_14-40-34.log")
df = parser.get_pd()
print(df.head())