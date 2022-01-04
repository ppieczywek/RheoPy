import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import wx


def herschel_bulkley_model(x, G, K, n):
    return G + K * (x**n)


def power_law_model(x, K, n):
    return K * (x**n)


yield_data = []
viscosity_data = []
hb_model_data = []
pl_model_data = []
tx_data = []


print("\n\tTA Instruments rheometer data analysis script - v.1.0 \n")

app = wx.App()
frame = wx.Frame(None, -1, 'RheoData.py')
frame.SetSize(0, 0, 200, 50)

# Create open file dialog
openFileDialog = wx.FileDialog(frame, "Open", "", "",
                               "Select DHR-1 rheometer output data files (*.txt)|*.txt",
                               wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

openFileDialog.ShowModal()
files = openFileDialog.GetPaths()
openFileDialog.Destroy()


for file in files:

    file_path = file
    file_name = file_path.split('\\')[-1]

    data_file = open(file_path, 'r')
    text_lines = data_file.readlines()

    print(f"\tProcessing data from file: {file_name}")

    data_block_positions = []

    # określić data block name, size, position, col_num,
    line_num = 0
    for line in text_lines:
        if "[step]" in line.lower():
            data_block_positions.append(line_num)

        line_num += 1

    if data_block_positions:
        for i in range(len(data_block_positions)):

            block_name = text_lines[data_block_positions[i] + 1].lower().rstrip()

            if "flow ramp" in block_name:
                headers = (text_lines[data_block_positions[i] + 2].rstrip()
                           ).lower().replace(" ", "_").split(sep="\t")
                if set(['shear_rate', 'stress', 'viscosity']).issubset(headers):
                    if i == (len(data_block_positions) - 1):
                        chunk_size = len(text_lines) - (data_block_positions[i] + 4)
                    else:
                        chunk_size = (data_block_positions[i+1] - 1) - \
                                     (data_block_positions[i] + 4)

                    data_block = pd.read_csv(file_path, sep="\t",
                                             skiprows=data_block_positions[i] + 4,
                                             nrows=chunk_size,
                                             decimal=",",
                                             header=None)
                    data_block.columns = headers

                    stress_max_loc = data_block['viscosity'].argmax()
                    if stress_max_loc == 0:
                        record = {'file': file_name,
                                  'step': block_name,
                                  'yield_stress': 0,
                                  }
                    else:
                        record = {'file': file_name,
                                  'step': block_name,
                                  'yield_stress': data_block['stress'].iloc[stress_max_loc],
                                  }
                    yield_data.append(record)
                else:
                    print(f"{file_name} error: shear_rate, stress or viscosity data not found")

            if "peak hold" in block_name:
                headers = (text_lines[data_block_positions[i] + 2].rstrip()
                           ).lower().replace(" ", "_").split(sep="\t")
                if set(['shear_rate', 'stress', 'viscosity']).issubset(headers):
                    if i == (len(data_block_positions) - 1):
                        chunk_size = len(text_lines) - (data_block_positions[i] + 4)
                    else:
                        chunk_size = (data_block_positions[i+1] - 1) - (data_block_positions[i] + 4)

                    data_block = pd.read_csv(file_path, sep="\t",
                                             skiprows=data_block_positions[i] + 4,
                                             nrows=chunk_size,
                                             decimal=",",
                                             header=None)

                    data_block.columns = headers
                    data_block = data_block.iloc[3:-3]
                    data_block_mean = data_block.mean(axis='columns')
                    record = {'file': file_name,
                              'step': block_name,
                              'shear_rate': data_block['shear_rate'].mean(),
                              'viscosity': data_block['viscosity'].mean(),
                              }
                    viscosity_data.append(record)
                else:
                    print(f"{file_name} error: shear_rate, stress or viscosity data not found")

            if "flow sweep" in block_name:
                headers = (text_lines[data_block_positions[i] + 2].rstrip()
                           ).lower().replace(" ", "_").split(sep="\t")
                if set(['shear_rate', 'stress']).issubset(headers):

                    chunk_size = 0
                    if i == (len(data_block_positions) - 1):
                        chunk_size = len(text_lines) - (data_block_positions[i] + 4)
                    else:
                        chunk_size = (data_block_positions[i+1] - 1) - (data_block_positions[i] + 4)

                    data_block = pd.read_csv(file_path, sep="\t",
                                             skiprows=data_block_positions[i] + 4,
                                             nrows=chunk_size,
                                             decimal=",",
                                             header=None)

                    data_block.columns = headers
                    data_block.sort_values(by='shear_rate', inplace=True)

                    area = np.trapz(y=data_block['stress'].values,
                                    x=data_block['shear_rate'].values)

                    record = {'file': file_name,
                              'step': block_name,
                              'area': area}
                    tx_data.append(record)

                    try:
                        hb_popt, hb_pcov = curve_fit(herschel_bulkley_model,
                                                     xdata=data_block['shear_rate'].values,
                                                     ydata=data_block['stress'].values,
                                                     maxfev=3000,
                                                     p0=[1, 2, 0.7],
                                                     bounds=((0.0, 0.00001, 0.00001), (1000, 1000, 100)))

                        hb_residuals = data_block['stress'].values - \
                            herschel_bulkley_model(data_block['shear_rate'].values, *hb_popt)
                        hb_ss_res = np.sum(hb_residuals**2)
                        hb_ss_tot = np.sum(
                            (data_block['stress'].values - np.mean(data_block['stress'].values))**2)
                        hb_r_squared = 1 - (hb_ss_res / hb_ss_tot)

                        a, b, c = hb_popt
                        record = {'file': file_name,
                                  'step': block_name,
                                  'G0': a,
                                  'K': b,
                                  'n': c,
                                  'R2': hb_r_squared}
                        hb_model_data.append(record)

                    except RuntimeError:
                        print(f"\t{file_name} error: Hershel-Buckley curve_fit failed\n")
                        record = {'file': file_name,
                                  'step': block_name,
                                  'G0': -99999.9,
                                  'K': -99999.9,
                                  'n': -99999.9,
                                  'R2': -99999.9}
                        hb_model_data.append(record)

                    try:
                        pl_popt, pl_pcov = curve_fit(power_law_model,
                                                     xdata=data_block['shear_rate'].values,
                                                     ydata=data_block['stress'].values,
                                                     maxfev=3000,
                                                     p0=[2, 0.7],
                                                     bounds=((0.0001, 0.000001), (1000, 100)))

                        pl_residuals = data_block['stress'].values - \
                            power_law_model(data_block['shear_rate'].values, *pl_popt)
                        pl_ss_res = np.sum(pl_residuals**2)
                        pl_ss_tot = np.sum(
                            (data_block['stress'].values - np.mean(data_block['stress'].values))**2)
                        pl_r_squared = 1 - (pl_ss_res / pl_ss_tot)

                        a, b = pl_popt
                        record = {'file': file_name,
                                  'step': block_name,
                                  'K': a,
                                  'n': b,
                                  'R2': pl_r_squared}
                        pl_model_data.append(record)

                    except RuntimeError:
                        print(f"\t{file_name} error: Ostwald curve_fit failed\n")
                        record = {'file': file_name,
                                  'step': block_name,
                                  'K': -99999.9,
                                  'n': -99999.9,
                                  'R2': -99999.9}
                        pl_model_data.append(record)
                else:
                    print(f"{file_name} error: shear_rate, stress or viscosity data not found")

    else:
        print(f"\t{file_name} error - corrupted data blocks or data blocks not present in file.\n")

save_file_dialog = wx.FileDialog(frame, "Save data to Excel file",
                                 wildcard="xlsx files (*.xlsx)|*.xlsx",
                                 style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

save_file_dialog.ShowModal()
xlsx_file = save_file_dialog.GetPath()
save_file_dialog.Destroy()

if xlsx_file:
    with pd.ExcelWriter(xlsx_file) as writer:

        if yield_data:
            pd.DataFrame(yield_data).to_excel(writer, sheet_name='Yield')

        if viscosity_data:
            pd.DataFrame(viscosity_data).to_excel(writer, sheet_name='Viscosity')

        if pl_model_data:
            pd.DataFrame(pl_model_data).to_excel(writer, sheet_name='Ostwald')

        if hb_model_data:
            pd.DataFrame(hb_model_data).to_excel(writer, sheet_name='Hershel-Buckley')

        if tx_data:
            pd.DataFrame(tx_data).to_excel(writer, sheet_name='Thixotropy')

else:
    print("\n\tUnable to create MS Excel file.\n")

frame.Destroy()
app.Destroy()
input("\tPress Enter to continue...")
