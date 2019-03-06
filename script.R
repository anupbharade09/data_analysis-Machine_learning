# --------------------------------------------
# get the libraries
# --------------------------------------------
library(reticulate)
library(RColorBrewer)
install.packages("pander")
library(pander)
library(magrittr)
library(xcms)

# Provide location of raw cdf files
path_to_raw_data <- "/Users/anupbharade/Desktop/standard_mixture/raw_data/27_compounds/Guanosine/data/"

# # For your own raw data files, specify the folder
#path_to_raw_data <- "/Users/anupbharade/Desktop/standard_mixture/raw_data"
all_raw_files <- list.files(path_to_raw_data, recursive=T, full.names=T)

# set up the working directory
#setwd("/Users/xdu4/Documents/Duxiuxia/Analysis/UAB_workshop_2018/XCMS_analysis/")


pd <- data.frame(sample_name=sub(basename(all_raw_files),
                                 pattern = ".CDF", 
                                 replacement = "", 
                                 fixed = TRUE),
                 sample_group = c(rep("KO", 7)),
                 stringsAsFactors = FALSE) 

# --------------------------------------------
# import raw data
# --------------------------------------------
# get file path and names

raw_data <- readMSData(files=all_raw_files, 
                       pdata=new("NAnnotatedDataFrame", pd), 
                       mode="onDisk")

#BPCs <- chromatogram(raw_data, aggregationFun="max")
#BPC_1 <- BPCs[[1]]
#plot(BPC_1, type='l', col='red')

rtrange <- c(min(rtime(raw_data)),max(rtime(raw_data)))
mzrange <- c(72.9, 73.1)

# define colors for the two groups
group_colors <- brewer.pal(3, "Set1")[1:2]
names(group_colors) <- c("KO", "WT")


## extract the chromatogram
chr_raw <- chromatogram(raw_data, mz = mzrange, rt = rtrange)


# *** obiwarp alignment
obiwarp_parameters <- ObiwarpParam(binSize=0.6)

# *** specify centWave parameters
cwt_parameters <- CentWaveParam(peakwidth=c(1,5),
                                ppm=6,
                                noise=100,snthresh=0)


xdata <- findChromPeaks(raw_data, 
                        param=cwt_parameters)

xdata <- adjustRtime(xdata, param=obiwarp_parameters)

## extract the chromatogram
chr_raw_after <- chromatogram(xdata, mz = mzrange, rt = rtrange)

plot(chr_raw, col = group_colors[chr_raw$sample_group])

plot(chr_raw_after, col = "black",add= TRUE,type="l", lty=2,main=NULL)


legend("topleft", 
       legend=c("Before alignment","After alignment"), 
       col = c('red','black'), 
       lty = c(1,2), 
       lwd=c(2.5,2.5), 
       text.col = "black", 
       horiz = F , 
       inset = c(0.1, 0.1))


title(main= NULL,sub = "Before and After alignment - Guanosine")

