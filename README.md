# ret2018software
This is the software associated with the 2018 Research Experience for Teachers at Haystack Observatory using Software Defined Radios and UASs.

### UAS related software:
  We have developed specific software to extract the information from .BIN or .ulg drone flight data files. We have identified the parameters we want to extract, in particular GPS coordinates and timestamp, and used some already available packages to extract such information into .CSV files.
  We have developed some methods to read such .CSV file and transform from GPS Lat, Lon, Alt coordinates into ECEF (Earth Centered Earth Fix) coordinates and later on from ECEF coordinates into ENU (East North Up) in the tangent local plane (TLP). We have also created a method to calculate the velocity and the acceleration in the trajectory.
  Finally, we have created some methods to plot the trajectory and choose to plot the vector velocity and the acceleration in 3D.
  Each method can be run independently of the main program that performs all the above operations at once.
  
  The organiztion of the software could be undertood as:
  
  - [ ] Transform a .BIN or .ulg file into a .CSV file.
  - [ ] Read the .CSV file from one or the other format originally, and clean it into a standard way of organizing columns before transformation.
  - [ ] Perform a GPS- Lat, Lon, Alt to ECEF transformation.
  - [ ] Perform a ECEF to ENU transformation.
  - [ ] Calculate velocity.
  - [ ] Calculate acceleration.
  - [ ] Plot Trajectory, with or without the velocity and/or acceleration vectors in 3D.
