os.chdir(
    r"C:\Users\bras2428\Desktop\AleTest"
)  # change to the directory containing the file.
dset = (
    QTLab_Dataset.find()
)  # this finds all datasets labelled in a certain way, I renamed your file so the regular expression matching works to: 172335_Ale01_IVsVg_r31.dat_
print(
    dset
)  # this shows how the load method splits the filename up to make a list of dictionaries.
data = dset.load(
    Stability_Diagram, axes=("Vg", "T", "Vsd", "Isd", "t")
)  # the methods Bart and me wrote for stability diagrams assume that the axes are labelled in this way (not Vsd_mV, and Vg_V, etc.. as they are in the text file)
dataSD = data[0]  # the SD is a pandas dataframe that is the first item

T = np.mean(
    dataSD["T"].values
)  # i took the temperature of the measurement as the mean of all the values of temperature recording during the stability diagram
print(
    "Stability diagram measured at {:.1f} K".format(T)
)  # print the temperature to 1 decimal place
# dataSD.resample(512, 512)  # resample is a useful tool to make your data more manageable for some of the methods, especially when you are just playing around with the data and script at first, you can remove this line for the final figure!
dataSD["Vsd"] = (
    1e-3 * dataSD["Vsd"].values
)  # the methods want us to work in V (not mV) so this changes the Vsd values to V
dataSD.correct_offset()  # this is a stability diagram method can be found in qtlab_data file, it takes each I-Vsd trace and subtracts the I at around zero - see the method for exactly how it works!

gatetrace = (
    dataSD.zero_bias_gate_trace()
)  # this method generate a zero-bias condutance gate trace, again see the stability diagram class in qtlab_data for exactly how it works
fig = Figure()  # make a figure object, you can define things like aspect ratio and size
fig.add_subplot(Subplot_IVsVg(dataSD))  # plot the SD
fig.add_subplot(Subplot_GVsVg(dataSD))  # plot the conductance SD
fig.add_subplot(Subplot_GVg(gatetrace))  # plot the conductance gate trace
fig.visualise()  # see the plot - enter a file name as a string to export it e.g. 'test.pdf'
#####
# raise SystemExit  # Ale  - you can comment out this line if you want to see a fit to your data below
####
vcs = [
    -17.97,
    -12.16,
    -6.25,
    -0.81,
    3.69,
    8.67,
    15.05,
]  # a list I made of approximate peak positions using manual_fit_vc stability diagram method
alpha = 0.023  # starting value for alpha as 23 meV/V as you have already told me
gatetraceFits = []  # an empty list to add the gate trace fits to in the for loop

for vc in vcs:  # loop over the peaks values
    dat2 = dataSD.copy()  # make a new copy of the data for each iteration
    setdct = {"Vc": vc, "T": T}  # make a dictionary with vc and T
    dat2.ps(
        **setdct
    )  # add vc and T to the .ps of the data (the ps contains a dictionary of variables associated with the data)
    dat2 = dat2[
        dat2["Vg"] > (vc - 3)
    ]  # define a range of the stability diagram to focus on, as the peaks are spaced around 6-7 Vg apart, I chose the range to be the peak +/-3 V, to avoid overlap
    dat2 = dat2[dat2["Vg"] < (vc + 3)]
    gMaxTemp = gatetrace["Gsd"][
        (np.argmin(np.abs(gatetrace["Vg"].values - vc)))
    ]  # this is a bit hard to read but it tells us the Gsd at the voltage: vc. We will take this as the initial guess for Gmax for the fitting
    print("Max Gsd in this window: {:.3e} S".format(gMaxTemp))  # print the Gmax
    p0 = {
        "Vc": vc,
        "Gmax": gMaxTemp,
        "alpha": alpha,
    }  # set the initial values as a dictionary
    bounds = [
        (vc - 1, 0.5, 0.85 * alpha),
        (vc + 1, 1.5, 1.15 * alpha),
    ]  # set bounds for the fitting parameters for vc, gmax and alpha. They can be a bit abitrary to find what works. The Gmax is normalized to equal 1 in the function so the bounds are 0.5*Gmax to 1.5 Gmax really
    params, r = dat2.fit_coulomb_peak(
        p0=p0, bounds=bounds
    )  # this is the function that fits the data - find the method in qtlab_data and the function in physics_models
    print(
        "Final parameters for peak: alpha_gate = {:.3f} meV/V, Gmax = {:.3e} S, Peak position: {:.3f} Vg".format(
            params["alpha"], params["Gmax"], params["Vc"]
        )
    )  # print the optimised parameters
    params["T"] = T  # add the temperature to the the dictionary of parameters
    vg = gatetrace["Vg"].values  # this is an array of the gate voltages
    fitGsd = physics_models.thermal_broadening(
        vg, **params
    )  # use the optimised parameters and the gate voltage array to generate the Gsd fit values
    gatetraceFit = gatetrace.copy()  # make a copy of the gate trace
    gatetraceFit["Gsd"] = fitGsd  # replace the Gsd data with the fitted data
    try:
        gatetraceFits.append(gatetraceFit)  # add the fitted gate trace to the list
    except:
        pass

gatetraceFitSum = gatetrace.copy()  # make another copy of the gate trace to play with
gatetraceFitSum["Gsd"] -= gatetraceFitSum[
    "Gsd"
].values  # make the Gsd values equal to themselves minus themselves, i.e. make them zero!
for fit in gatetraceFits:  # loop over the fits we added to this list
    gatetraceFitSum["Gsd"] += fit[
        "Gsd"
    ].values  # add the fit values one by one to generate a sum of fits

gatetraceFitSum.ps(
    color="black", label="sum of fits", linewidth=2
)  # change some of the plotting parameters to make it obvious which one is the sum

fig = Figure()  # make a figure
fig.add_subplot(
    Subplot_GVg(gatetrace, *gatetraceFits, gatetraceFitSum, legend=True)
)  # plot the experimental gate traces, and the list of fits all together
fig.visualise()  # visualise, or save
