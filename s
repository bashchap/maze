export PATH="./:$PATH"

python3 mk_plot_data.py
python3 plot3d.py &
python3 plot2d.py &
