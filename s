export PATH="./:$PATH"

/opt/homebrew/opt/python3/bin/python3 mk_plot_data.py
/opt/homebrew/opt/python3/bin/python3 plot3d.py &
/opt/homebrew/opt/python3/bin/python3 plot2d.py &
