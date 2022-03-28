import numpy as np
import pandas as pd
from util.singleton import *


@singleton
class indicator_caculator():
	def RSI(self, df, period):
		date_index = df.index.astype('str')
		# df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 넣고, 감소했으면 0을 넣어줌
		U = np.where(df['close'].diff(1) > 0, df['close'].diff(1), 0)
		# df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 넣고, 증가했으면 0을 넣어줌
		D = np.where(df['close'].diff(1) < 0, df['close'].diff(1) * (-1), 0)
		AU = pd.DataFrame(U, index=date_index).rolling(window=period).mean()  # AU, period=2일 동안의 U의 평균
		AD = pd.DataFrame(D, index=date_index).rolling(window=period).mean()  # AD, period=2일 동안의 D의 평균
		RSI = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함

		return RSI
