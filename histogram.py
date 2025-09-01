# 
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# import os
# input_folder = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\hist_data\nanopore_histrogram'
# 
# for filename in os.listdir(input_folder):
#     if filename.endswith('.csv'):
#         file_path = os.path.join(input_folder, filename)
#         try:
#             hist = pd.read_csv(file_path, sep=',',header = 0)
#             plot_label_name = file_path.split('\\')[-1]
# 
#             fig,ax = plt.subplots(1, 1,figsize=(20,10))
#             counts = hist['counts'].tolist()
#             bins_pos = hist['bins'].round(2).astype(str)
#             plt.bar(bins_pos,counts,color ='blue')
#             tick_spacing  = 1
#             ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
#             plt.xticks(fontsize =5)
#             plt.xlabel("Bin_size")
#             plt.ylabel("counts")
#             plt.title(plot_label_name)
#             #   plt.show()
#             plt_name = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\hist_data\plots_nanopore\\' + plot_label_name + '.png'
#             plt.savefig(plt_name)
#             plt.close()
#         except Exception as e:
#             print(f"Error processing {filename}: {e}")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import os

input_folder = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\hist_data\pacbio_histrogram'
output_pdf = r'C:\Users\Samuel\OneDrive - Drexel University\Dr. Xiao Scripts Coop 2025\hist_data\pacbio_histograms.pdf'

with PdfPages(output_pdf) as pdf:
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(input_folder, filename)
            try:
                hist = pd.read_csv(file_path, sep=',',header = 0)
                plot_label_name = file_path.split('\\')[-1]

                fig,ax = plt.subplots(1, 1,figsize=(20,10))
                counts = hist['counts'].tolist()
                bins_pos = hist['bins'].round(2).astype(str)
                plt.bar(bins_pos,counts,color ='blue')
                tick_spacing  = 1
                ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
                plt.xticks(fontsize =5)
                plt.xlabel("Bin_size")
                plt.ylabel("counts")
                plt.title(plot_label_name)
                #   plt.show()
                pdf.savefig(fig)
                plt.close(fig)

            except Exception as e:
                print(f"Error processing {filename}: {e}")

print(f"\n✅ All nanopore histograms saved to: {output_pdf}")
