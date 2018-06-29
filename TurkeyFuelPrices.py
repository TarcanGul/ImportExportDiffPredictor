from matplotlib import pyplot as plt
import pandas as pd
import quandl
from sklearn.tree import DecisionTreeRegressor
from sklearn import model_selection

"""
The program predicts the import-export difference using the gasoline prices. The reasoning behind this relationship is
that (my hypothesis) 1- One of Turkey's major import is petroleum and 2- Gasoline price is also a factor for other 
imports because of transportation needs. 
"""
while True:
    try:
        inp = float(input(
            "Enter a gasoline price to estimate the difference between import and export(Turkish Liras)[r: 1-15]: "))
        if 1 <= inp <= 15:
            break
        else:
            print("Not in range. Try again!")
            continue
    except ValueError:
        print("Not valid. Try again!")
        continue


fig, ax = plt.subplots()

difference_data = pd.read_excel('TurkeyImportExportDataOptimized.xlsx', headers=None)
gasoline_data = quandl.get("GPP/CFP_TUR", authtoken="YtQfZxtvQT_7-xvX4zj4",
                           start_date="2016-08-20", end_date="2018-04-01")

plt.subplot(311)
plt.plot(gasoline_data['Gasoline Price'], label="Prices (Turkish Liras)", color="m")
plt.title("Gasoline Price in Turkey vs. Export-Import Difference")
plt.legend()

plt.subplot(312)
plt.plot(gasoline_data['Gasoline One-Week Change %'], label="One week changes of gasoline prices (%)", color='g')
plt.legend()

plt.subplot(313)
plt.plot(difference_data['Month'].get_values(), difference_data['Export-Import Difference'])
plt.legend()
fig.autofmt_xdate()

reg = DecisionTreeRegressor()
data_trimmed = gasoline_data['Gasoline Price']['2016-08-04'::21]
print(data_trimmed)
x_train, x_test, y_train, y_test = model_selection.train_test_split(data_trimmed.to_frame(), difference_data['Export-Import Difference'].to_frame())
reg.fit(x_train, y_train)
print("Prediction of export-import difference: ", reg.predict(inp))

plt.show()



