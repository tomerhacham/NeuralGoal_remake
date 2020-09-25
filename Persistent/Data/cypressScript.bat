@echo off

set fileName=%1

cd "C:\Users\Andrey\Documents\NeuralGoal_remake\Persistent\Data\NeuralGoalCypress"
echo %cd%

npm run cy:run -- --spec C:\Users\Andrey\Documents\NeuralGoal_remake\Persistent\Data\NeuralGoalCypress\cypress\integration\examples\%fileName%.js