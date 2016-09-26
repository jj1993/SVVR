#!/usr/bin/env python

import vtk, time

# Set up renderer, render window and interactor
ren = vtk.vtkRenderer()
renwin = vtk.vtkRenderWindow()
renwin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

"""
Following code based on vtk example from: 
http://www.vtk.org/gitweb?p=VTK.git;a=blob_plain;f=Examples/Medical/Python/Medical1.py
"""

# # Reading data
# reader = vtk.vtkRectilinearGridReader()
# reader.SetFileName("data/wervel.vtk")
# reader.Update()

reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("data/wervel.vtk")
reader.Update()

seeds = vtk.vtkPointSource()
seeds.SetRadius(3)
seeds.SetNumberOfPoints(50)
seeds.SetCenter(reader.GetOutput().GetCenter())

integ = vtk.vtkRungeKutta4()

streamer = vtk.vtkStreamTracer()
streamer.SetInputConnection(reader.GetOutputPort())
streamer.SetSourceConnection(seeds.GetOutputPort())
streamer.SetMaximumPropagation(30)
streamer.SetInitialIntegrationStep(0.1)
streamer.SetIntegrationDirectionToBoth()
streamer.SetIntegrator(integ)

mapStreamLines = vtk.vtkPolyDataMapper()
mapStreamLines.SetInputConnection(streamer.GetOutputPort())
mapStreamLines.SetScalarRange(reader.GetOutput().GetScalarRange())

streamLineActor = vtk.vtkActor()
streamLineActor.SetMapper(mapStreamLines)

# An outline provides context around the data.
outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(reader.GetOutputPort())
mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())
outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(.5, .5, .5)

# An initial camera position is defined
"""
WERKT NIET...?!
"""
camera = vtk.vtkCamera()
camera.SetViewUp(0, -1, 0)
camera.SetPosition(50, 50, 150)
camera.SetFocalPoint(0, 0, 0)
camera.ComputeViewPlaneNormal()

# The actors and camera are added to the renderer
# The background colour is set
ren.SetBackground(0,0,0)
ren.AddActor(outline)
# ren.SetActiveCamera(camera)
ren.AddActor(streamLineActor)

# The size of the renderer window is set
renwin.SetSize(640, 480)

# Set interactor style to trackball
istyle = vtk.vtkInteractorStyleSwitch()
iren.SetInteractorStyle(istyle)
istyle.SetCurrentStyleToTrackballCamera()

# Lets go! :D
iren.Initialize()
renwin.Render()
iren.Start()