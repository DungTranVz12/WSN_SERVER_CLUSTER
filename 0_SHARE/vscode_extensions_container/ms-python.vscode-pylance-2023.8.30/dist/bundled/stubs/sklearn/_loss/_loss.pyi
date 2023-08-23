
class CyLossFunction:
    def cy_loss(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_gradient(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_grad_hess(self, y_true: float, raw_prediction: float)->tuple[float,float]: ...


class CyHalfSquaredError(CyLossFunction):
    def cy_loss(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_gradient(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_grad_hess(self, y_true: float, raw_prediction: float)->tuple[float,float]: ...


class CyAbsoluteError(CyLossFunction):
    def cy_loss(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_gradient(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_grad_hess(self, y_true: float, raw_prediction: float)->tuple[float,float]: ...


class CyPinballLoss(CyLossFunction):
    quantile: float
    def cy_loss(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_gradient(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_grad_hess(self, y_true: float, raw_prediction: float)->tuple[float,float]: ...


class CyHalfPoissonLoss(CyLossFunction):
    def cy_loss(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_gradient(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_grad_hess(self, y_true: float, raw_prediction: float)->tuple[float,float]: ...


class CyHalfGammaLoss(CyLossFunction):
    def cy_loss(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_gradient(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_grad_hess(self, y_true: float, raw_prediction: float)->tuple[float,float]: ...


class CyHalfTweedieLoss(CyLossFunction):
    power: float
    def cy_loss(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_gradient(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_grad_hess(self, y_true: float, raw_prediction: float)->tuple[float,float]: ...


class CyHalfTweedieLossIdentity(CyLossFunction):
    power: float
    def cy_loss(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_gradient(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_grad_hess(self, y_true: float, raw_prediction: float)->tuple[float,float]: ...

    
class CyHalfBinomialLoss(CyLossFunction):
    def cy_loss(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_gradient(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_grad_hess(self, y_true: float, raw_prediction: float)->tuple[float,float]: ...

    
class CyHalfMultinomialLoss(CyLossFunction):
    def cy_loss(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_gradient(self, y_true: float, raw_prediction: float) -> float: ...
    def cy_grad_hess(self, y_true: float, raw_prediction: float)->tuple[float,float]: ...


