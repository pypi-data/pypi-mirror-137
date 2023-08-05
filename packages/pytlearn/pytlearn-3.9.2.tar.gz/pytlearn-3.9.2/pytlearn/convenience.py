# import the necessary packages
import numpy as np
import cv2
import sys

# import any special Python 2.7 packages
if sys.version_info.major == 2:
    from urllib import urlopen

# import any special Python 3 packages
elif sys.version_info.major == 3:
    from urllib.request import urlopen


class NuSVCModel():
    """Nu-Support Vector Classification.

    Similar to SVC but uses a parameter to control the number of support
    vectors.

    The implementation is based on libsvm.

    Read more in the :ref:`User Guide <svm_classification>`.

    Parameters
    ----------
    nu : float, default=0.5
        An upper bound on the fraction of margin errors (see :ref:`User Guide
        <nu_svc>`) and a lower bound of the fraction of support vectors.
        Should be in the interval (0, 1].

    kernel : {'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'}, default='rbf'
         Specifies the kernel type to be used in the algorithm.
         It must be one of 'linear', 'poly', 'rbf', 'sigmoid', 'precomputed' or
         a callable.
         If none is given, 'rbf' will be used. If a callable is given it is
         used to precompute the kernel matrix.

    degree : int, default=3
        Degree of the polynomial kernel function ('poly').
        Ignored by all other kernels.

    gamma : {'scale', 'auto'} or float, default='scale'
        Kernel coefficient for 'rbf', 'poly' and 'sigmoid'.

        - if ``gamma='scale'`` (default) is passed then it uses
          1 / (n_features * X.var()) as value of gamma,
        - if 'auto', uses 1 / n_features.

        .. versionchanged:: 0.22
           The default value of ``gamma`` changed from 'auto' to 'scale'.

    coef0 : float, default=0.0
        Independent term in kernel function.
        It is only significant in 'poly' and 'sigmoid'.

    shrinking : bool, default=True
        Whether to use the shrinking heuristic.
        See the :ref:`User Guide <shrinking_svm>`.

    probability : bool, default=False
        Whether to enable probability estimates. This must be enabled prior
        to calling `fit`, will slow down that method as it internally uses
        5-fold cross-validation, and `predict_proba` may be inconsistent with
        `predict`. Read more in the :ref:`User Guide <scores_probabilities>`.

    tol : float, default=1e-3
        Tolerance for stopping criterion.

    cache_size : float, default=200
        Specify the size of the kernel cache (in MB).

    class_weight : {dict, 'balanced'}, default=None
        Set the parameter C of class i to class_weight[i]*C for
        SVC. If not given, all classes are supposed to have
        weight one. The "balanced" mode uses the values of y to automatically
        adjust weights inversely proportional to class frequencies as
        ``n_samples / (n_classes * np.bincount(y))``

    verbose : bool, default=False
        Enable verbose output. Note that this setting takes advantage of a
        per-process runtime setting in libsvm that, if enabled, may not work
        properly in a multithreaded context.

    max_iter : int, default=-1
        Hard limit on iterations within solver, or -1 for no limit.

    decision_function_shape : {'ovo', 'ovr'}, default='ovr'
        Whether to return a one-vs-rest ('ovr') decision function of shape
        (n_samples, n_classes) as all other classifiers, or the original
        one-vs-one ('ovo') decision function of libsvm which has shape
        (n_samples, n_classes * (n_classes - 1) / 2). However, one-vs-one
        ('ovo') is always used as multi-class strategy. The parameter is
        ignored for binary classification.

        .. versionchanged:: 0.19
            decision_function_shape is 'ovr' by default.

        .. versionadded:: 0.17
           *decision_function_shape='ovr'* is recommended.

        .. versionchanged:: 0.17
           Deprecated *decision_function_shape='ovo' and None*.

    break_ties : bool, default=False
        If true, ``decision_function_shape='ovr'``, and number of classes > 2,
        :term:`predict` will break ties according to the confidence values of
        :term:`decision_function`; otherwise the first class among the tied
        classes is returned. Please note that breaking ties comes at a
        relatively high computational cost compared to a simple predict.

        .. versionadded:: 0.22

    random_state : int or RandomState instance, default=None
        Controls the pseudo random number generation for shuffling the data for
        probability estimates. Ignored when `probability` is False.
        Pass an int for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Attributes
    ----------
    support_ : ndarray of shape (n_SV,)
        Indices of support vectors.

    support_vectors_ : ndarray of shape (n_SV, n_features)
        Support vectors.

    n_support_ : ndarray of shape (n_class), dtype=int32
        Number of support vectors for each class.

    dual_coef_ : ndarray of shape (n_class-1, n_SV)
        Dual coefficients of the support vector in the decision
        function (see :ref:`sgd_mathematical_formulation`), multiplied by
        their targets.
        For multiclass, coefficient for all 1-vs-1 classifiers.
        The layout of the coefficients in the multiclass case is somewhat
        non-trivial. See the :ref:`multi-class section of the User Guide
        <svm_multi_class>` for details.

    coef_ : ndarray of shape (n_class * (n_class-1) / 2, n_features)
        Weights assigned to the features (coefficients in the primal
        problem). This is only available in the case of a linear kernel.

        `coef_` is readonly property derived from `dual_coef_` and
        `support_vectors_`.

    intercept_ : ndarray of shape (n_class * (n_class-1) / 2,)
        Constants in decision function.

    classes_ : ndarray of shape (n_classes,)
        The unique classes labels.

    fit_status_ : int
        0 if correctly fitted, 1 if the algorithm did not converge.

    probA_ : ndarray of shape (n_class * (n_class-1) / 2,)
    probB_ : ndarray of shape (n_class * (n_class-1) / 2,)
        If `probability=True`, it corresponds to the parameters learned in
        Platt scaling to produce probability estimates from decision values.
        If `probability=False`, it's an empty array. Platt scaling uses the
        logistic function
        ``1 / (1 + exp(decision_value * probA_ + probB_))``
        where ``probA_`` and ``probB_`` are learned from the dataset [2]_. For
        more information on the multiclass case and training procedure see
        section 8 of [1]_.

    class_weight_ : ndarray of shape (n_class,)
        Multipliers of parameter C of each class.
        Computed based on the ``class_weight`` parameter.

    shape_fit_ : tuple of int of shape (n_dimensions_of_X,)
        Array dimensions of training vector ``X``.

    Examples
    --------

    [1]

    See also
    --------
    SVC
        Support Vector Machine for classification using libsvm.

    LinearSVC
        Scalable linear Support Vector Machine for classification using
        liblinear.

    References
    ----------
    .. [1] `LIBSVM: A Library for Support Vector Machines
        <http://www.csie.ntu.edu.tw/~cjlin/papers/libsvm.pdf>`_

    .. [2] `Platt, John (1999). "Probabilistic outputs for support vector
        machines and comparison to regularizedlikelihood methods."
        <http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.41.1639>`_
    """

    _impl = 'nu_svc'

    def __init__(self, *, nu=0.5, kernel='rbf', degree=3, gamma='scale',
                 coef0=0.0, shrinking=True, probability=False, tol=1e-3,
                 cache_size=200, class_weight=None, verbose=False, max_iter=-1,
                 decision_function_shape='ovr', break_ties=False,
                 random_state=None):

        super().__init__(
            kernel=kernel, degree=degree, gamma=gamma,
            coef0=coef0, tol=tol, C=0., nu=nu, shrinking=shrinking,
            probability=probability, cache_size=cache_size,
            class_weight=class_weight, verbose=verbose, max_iter=max_iter,
            decision_function_shape=decision_function_shape,
            break_ties=break_ties,
            random_state=random_state)

    def _more_tags(self):
        return {
            '_xfail_checks': {
                'check_methods_subset_invariance':
                'fails for the decision_function method',
                'check_class_weight_classifiers': 'class_weight is ignored.'
            }
        }

    def pt(self):
        print("PT")


def translate(image, x, y):
    # define the translation matrix and perform the translation
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    # return the translated image
    return shifted


def rotate(image, angle, center=None, scale=1.0):
    # grab the dimensions of the image
    (h, w) = image.shape[:2]

    # if the center is None, initialize it as the center of
    # the image
    if center is None:
        center = (w // 2, h // 2)

    # perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    # return the rotated image
    return rotated


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w / 2, h / 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def skeletonize(image, size, structuring=cv2.MORPH_RECT):
    # determine the area (i.e. total number of pixels in the image),
    # initialize the output skeletonized image, and construct the
    # morphological structuring element
    area = image.shape[0] * image.shape[1]
    skeleton = np.zeros(image.shape, dtype="uint8")
    elem = cv2.getStructuringElement(structuring, size)

    # keep looping until the erosions remove all pixels from the
    # image
    while True:
        # erode and dilate the image using the structuring element
        eroded = cv2.erode(image, elem)
        temp = cv2.dilate(eroded, elem)

        # subtract the temporary image from the original, eroded
        # image, then take the bitwise 'or' between the skeleton
        # and the temporary image
        temp = cv2.subtract(image, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        image = eroded.copy()

        # if there are no more 'white' pixels in the image, then
        # break from the loop
        if area == area - cv2.countNonZero(image):
            break

    # return the skeletonized image
    return skeleton


def opencv2matplotlib(image):
    # OpenCV represents images in BGR order; however, Matplotlib
    # expects the image in RGB order, so simply convert from BGR
    # to RGB and return
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, readFlag)

    # return the image
    return image


def auto_canny(image, sigma=0.33, lst=None):
    # compute the median of the single channel pixel intensities
    if lst is None:
        lst = []
    # v = np.median(image)
    for flta in lst:
        if len(flta['data']['value']) == 0:
            lst.remove(flta)
    # apply automatic Canny edge detection using the computed median
    # lower = int(max(0, (1.0 - sigma) * v))
    # upper = int(min(255, (1.0 + sigma) * v))
    # edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return lst


def grab_contours(cnts):
    # if the length the contours tuple returned by cv2.findContours
    # is '2' then we are using either OpenCV v2.4, v4-beta, or
    # v4-official
    if len(cnts) == 2:
        cnts = cnts[0]

    # if the length of the contours tuple is '3' then we are using
    # either OpenCV v3, v4-pre, or v4-alpha
    elif len(cnts) == 3:
        cnts = cnts[1]

    # otherwise OpenCV has changed their cv2.findContours return
    # signature yet again and I have no idea WTH is going on
    else:
        raise Exception(("Contours tuple must have length 2 or 3, "
                         "otherwise OpenCV changed their cv2.findContours return "
                         "signature yet again. Refer to OpenCV's documentation "
                         "in that case"))

    # return the actual contours array
    return cnts


def is_cv2(or_better=False):
    # grab the OpenCV major version number
    major = get_opencv_major_version()

    # check to see if we are using *at least* OpenCV 2
    if or_better:
        return major >= 2

    # otherwise we want to check for *strictly* OpenCV 2
    return major == 2


def is_cv3(or_better=False):
    # grab the OpenCV major version number
    major = get_opencv_major_version()

    # check to see if we are using *at least* OpenCV 3
    if or_better:
        return major >= 3

    # otherwise we want to check for *strictly* OpenCV 3
    return major == 3


def is_cv4(or_better=False):
    # grab the OpenCV major version number
    major = get_opencv_major_version()

    # check to see if we are using *at least* OpenCV 4
    if or_better:
        return major >= 4

    # otherwise we want to check for *strictly* OpenCV 4
    return major == 4


def get_opencv_major_version(lib=None):
    # if the supplied library is None, import OpenCV
    if lib is None:
        import cv2 as lib

    # return the major version number
    return int(lib.__version__.split(".")[0])


def check_opencv_version(major, lib=None):
    # this function may be removed in a future release as we now
    # use the get_opencv_major_function to obtain the current OpenCV
    # version and then perform the actual version check *within* the
    # respective function
    import warnings
    message = """
        The check_opencv_version function is deprecated and may be
        removed in a future release. Use at your own risk.
    """
    warnings.warn(message, DeprecationWarning, stacklevel=2)

    # if the supplied library is None, import OpenCV
    if lib is None:
        import cv2 as lib

    # return whether or not the current OpenCV version matches the
    # major version number
    return lib.__version__.startswith(major)


def build_montages(image_list, image_shape, montage_shape):
    """
    ---------------------------------------------------------------------------------------------
    author: Kyle Hounslow
    ---------------------------------------------------------------------------------------------
    Converts a list of single images into a list of 'montage' images of specified rows and columns.
    A new montage image is started once rows and columns of montage image is filled.
    Empty space of incomplete montage images are filled with black pixels
    ---------------------------------------------------------------------------------------------
    :param image_list: python list of input images
    :param image_shape: tuple, size each image will be resized to for display (width, height)
    :param montage_shape: tuple, shape of image montage (width, height)
    :return: list of montage images in numpy array format
    ---------------------------------------------------------------------------------------------

    example usage:

    # load single image
    img = cv2.imread('lena.jpg')
    # duplicate image 25 times
    num_imgs = 25
    img_list = []
    for i in xrange(num_imgs):
        img_list.append(img)
    # convert image list into a montage of 256x256 images tiled in a 5x5 montage
    montages = make_montages_of_images(img_list, (256, 256), (5, 5))
    # iterate through montages and display
    for montage in montages:
        cv2.imshow('montage image', montage)
        cv2.waitKey(0)

    ----------------------------------------------------------------------------------------------
    """
    if len(image_shape) != 2:
        raise Exception('image shape must be list or tuple of length 2 (rows, cols)')
    if len(montage_shape) != 2:
        raise Exception('montage shape must be list or tuple of length 2 (rows, cols)')
    image_montages = []
    # start with black canvas to draw images onto
    montage_image = np.zeros(shape=(image_shape[1] * (montage_shape[1]), image_shape[0] * montage_shape[0], 3),
                             dtype=np.uint8)
    cursor_pos = [0, 0]
    start_new_img = False
    for img in image_list:
        if type(img).__module__ != np.__name__:
            raise Exception('input of type {} is not a valid numpy array'.format(type(img)))
        start_new_img = False
        img = cv2.resize(img, image_shape)
        # draw image to black canvas
        montage_image[cursor_pos[1]:cursor_pos[1] + image_shape[1], cursor_pos[0]:cursor_pos[0] + image_shape[0]] = img
        cursor_pos[0] += image_shape[0]  # increment cursor x position
        if cursor_pos[0] >= montage_shape[0] * image_shape[0]:
            cursor_pos[1] += image_shape[1]  # increment cursor y position
            cursor_pos[0] = 0
            if cursor_pos[1] >= montage_shape[1] * image_shape[1]:
                cursor_pos = [0, 0]
                image_montages.append(montage_image)
                # reset black canvas
                montage_image = np.zeros(
                    shape=(image_shape[1] * (montage_shape[1]), image_shape[0] * montage_shape[0], 3),
                    dtype=np.uint8)
                start_new_img = True
    if start_new_img is False:
        image_montages.append(montage_image)  # add unfinished montage
    return image_montages


def adjust_brightness_contrast(image, brightness=0., contrast=0.):
    """
    Adjust the brightness and/or contrast of an image

    :param image: OpenCV BGR image
    :param contrast: Float, contrast adjustment with 0 meaning no change
    :param brightness: Float, brightness adjustment with 0 meaning no change
    """
    beta = 0
    # See the OpenCV docs for more info on the `beta` parameter to addWeighted
    # https://docs.opencv.org/3.4.2/d2/de8/group__core__array.html#gafafb2513349db3bcff51f54ee5592a19
    return cv2.addWeighted(image,
                           1 + float(contrast) / 100.,
                           image,
                           beta,
                           float(brightness))