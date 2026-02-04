# STYLESHEET = """
# QMainWindow {
#     background-color: #2b2b2b;
# }

# /* General Text */
# QLabel, QCheckBox {
#     color: #e0e0e0;
#     font-size: 13px;
# }

# /* Group Boxes */
# QGroupBox {
#     background-color: #3c3f41;
#     border: 1px solid #555;
#     border-radius: 6px;
#     margin-top: 12px;
#     font-weight: bold;
#     color: #ffffff;
# }
# QGroupBox::title {
#     subcontrol-origin: margin;
#     left: 10px;
#     padding: 0 5px;
# }

# /* Buttons */
# QPushButton {
#     background-color: #4a4a4a;
#     color: #ffffff;
#     border: 1px solid #555;
#     padding: 6px 12px;
#     border-radius: 4px;
# }
# QPushButton:hover {
#     background-color: #5a5a5a;
#     border-color: #777;
# }
# QPushButton:disabled {
#     background-color: #333;
#     color: #777;
#     border-color: #444;
# }

# /* The special Green "Process" Button */
# QPushButton#processButton {
#     background-color: #2E8B57; /* SeaGreen */
#     border: none;
#     font-weight: bold;
# }
# QPushButton#processButton:hover {
#     background-color: #3CB371; /* MediumSeaGreen */
# }
# QPushButton#processButton:disabled {
#     background-color: #333;
#     color: #555;
# }

# /* Input Fields */
# QTextEdit, QLineEdit, QComboBox {
#     background-color: #1e1e1e;
#     color: #ffffff;
#     border: 1px solid #555;
#     border-radius: 3px;
#     padding: 4px;
# }

# /* Sliders */
# QSlider::groove:horizontal {
#     border: 1px solid #333;
#     height: 6px;
#     background: #1e1e1e;
#     margin: 2px 0;
#     border-radius: 3px;
# }
# QSlider::handle:horizontal {
#     background: #00ffff; /* Match map line color */
#     border: 1px solid #00cccc;
#     width: 14px;
#     height: 14px;
#     margin: -5px 0;
#     border-radius: 7px;
# }
# """

STYLESHEET = """
/* Standard Light Theme (Fusion) 
   We only style the Process Button to match your original look.
*/

QPushButton#processButton {
    background-color: #4CAF50;
    color: white;
    font-size: 14px;
    font-weight: bold;
    padding: 10px;
    border-radius: 5px;
}

QPushButton#processButton:hover {
    background-color: #45a049;
}

QPushButton#processButton:disabled {
    background-color: #cccccc;
    color: #666666;
}
"""