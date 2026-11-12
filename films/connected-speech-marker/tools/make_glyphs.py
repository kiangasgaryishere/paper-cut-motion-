"""Use the upstream MIT skeleton engine for the film's original English lettering."""
from pathlib import Path
import importlib.util
p=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('marker_skeleton',p/'upstream-skeleton.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
chars=''.join(chr(c) for c in range(33,127))+'→’'
module.FONTS={'Kalam700':('fonts/Kalam-Bold.ttf',chars),'Kalam400':('fonts/Kalam-Regular.ttf',chars)}
module.main()
