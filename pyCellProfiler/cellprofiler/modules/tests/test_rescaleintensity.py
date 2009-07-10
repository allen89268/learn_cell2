'''test_rescaleintensity.py - test the RescaleIntensity module

CellProfiler is distributed under the GNU General Public License.
See the accompanying file LICENSE for details.

Developed by the Broad Institute
Copyright 2003-2009

Please see the AUTHORS file for credits.

Website: http://www.cellprofiler.org
'''
__version__="$Revision$"

import base64
import numpy as np
import StringIO
import unittest
import zlib

import cellprofiler.pipeline as cpp
import cellprofiler.cpmodule as cpm
import cellprofiler.cpimage as cpi
import cellprofiler.measurements as cpmeas
import cellprofiler.objects as cpo
import cellprofiler.workspace as cpw

import cellprofiler.modules.rescaleintensity as R

INPUT_NAME = 'input'
OUTPUT_NAME = 'output'
REFERENCE_NAME = 'reference'
MEASUREMENT_NAME = 'measurement'

class TestRescaleIntensity(unittest.TestCase):
    def test_01_01_load_matlab_stretch(self):
        '''Load a pipeline with RescaleIntensity set up to stretch'''
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUXAuSk0s'
                'SU1RyM+zUnArylTwKs1RMDQAIitjUysTEwUjAwNLBZIBA6OnLz8DA0MwIwND'
                'xZy9ISf9DhsIzHXJjOxaJOP4aILy8W/8GtvlNFY4ioZvn8nmfXOKRUfRo8s/'
                'TB4d85Nd/UroVp9JUdqfe7MrbDbxMkwXZ4jdNy3PKVVWULrr8w3nYxkyT2Q3'
                'PAh7Uu89f1LPpMiOYCGxGc65RvZd4idvG63dPk94P0ehj5JozK0dHWkznupz'
                'e4rcXv+F27m/TtnE95DaD8/iWUea9L98zYk1T4yKnT3/cMz3gzcutM+b9PyH'
                'e8Tjtbw/pFnfd1Q0/ZzT8sJ+aq7V9r61Lz/cSJbc9LP9dnnkI75VMfXtfTcv'
                'GCZa2Oiez/jQI7qPN//CpPJTVZeuVDfWf6rreXzu49aw9uMmSoxskUFLfr+2'
                'mNV3+UJh5pvkLO3/pS+q1hXHZFrZfONU7jrjpd769vuCc963/3WWJ4gY9xSf'
                'mvbrTkn5FdPT6+Vk8vd9X5m+9UGk6ud3+x7tlb9xvV23ItPoP3veqZxrAHZa'
                'yfc=')
        pipeline = cpp.Pipeline()
        def callback(caller,event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO.StringIO(zlib.decompress(base64.b64decode(data))))
        self.assertEqual(len(pipeline.modules()), 1)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module, R.RescaleIntensity))
        self.assertEqual(module.image_name.value, "RescaledBlue")
        self.assertEqual(module.rescaled_image_name.value, "RescaledBlue")
        self.assertEqual(module.rescale_method, R.M_STRETCH)
    
    def test_01_02_load_matlab_enter_auto_low(self):
        '''Load a pipeline with automatic low manual scaling'''
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUXAuSk0s'
                'SU1RyM+zUnArylTwKs1RMDQAIisTAytTcwUjAwNLBZIBA6OnLz8DA0MLIwND'
                'xZy9U7z9DzkIHF/ue5C9zeTjos52OVvFCQIWXZ2dMi7MbRWxb5zMXmrXalR8'
                'WvzT8I9FXuL2HHPeWo85KZfOvfnz7/K5vNssDI85FvitP34l9EZU79GuB4U2'
                'RxM95qQGMPPqRfyb/YvnJ8tZXRvnsBZmj57n7ucO1UZWn7y0ONtNTE45WmeZ'
                'Wd8by2/Ny1nZb34yjkzM9rIzXNI73feDNWfHa4N5L0/fXLJe2qt29pX6K3dl'
                'pvRYmrTUxNRz767SXfzPZ8X1SJuDB6U3bah0P16SMbddZm6xp3rf+7kCv9t8'
                '50hLr+2x3Han/8nfW5ZVWV7+rQ83SF1/Jfp4i8hyx91X34Y+/iWdN+Hw1SWV'
                'Rwt3X3357UbNqo/Nds+/25qbT2y3L4o/lXj++8or6n2dvdMqXu6eGB7jPr3k'
                'y5Q+Rxnhat+HO0/F/X9t66cy18IssINlZm8f++/vjo1FvyeY2n+rl7h4/jan'
                'x45p531tl6/3ei8V8Ga3iOXce6VGO5T+buGa43by9Grd71FF665Xv9r58Y++'
                '17uiSgA7HuOs')
        pipeline = cpp.Pipeline()
        def callback(caller,event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO.StringIO(zlib.decompress(base64.b64decode(data))))                
        self.assertEqual(len(pipeline.modules()), 1)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module, R.RescaleIntensity))
        self.assertEqual(module.rescale_method, R.M_MANUAL_IO_RANGE)
        self.assertTrue(module.wants_automatic_low.value)
        self.assertFalse(module.wants_automatic_high.value)
        self.assertAlmostEqual(module.source_high.value, .5)
        self.assertAlmostEqual(module.dest_scale.min, .25)
        self.assertAlmostEqual(module.dest_scale.max, .75)
        self.assertAlmostEqual(module.custom_low_truncation.value, 0.125)
        self.assertAlmostEqual(module.custom_high_truncation.value, 0.875)
        self.assertEqual(module.low_truncation_choice.value, R.R_SET_TO_CUSTOM)
        self.assertEqual(module.high_truncation_choice.value, R.R_SET_TO_CUSTOM)
    
    def test_01_03_load_matlab_enter_auto_high(self):
        '''Load a pipeline with automatic high manual scaling'''
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUXAuSk0s'
                'SU1RyM+zUnArylTwKs1RMDQAIitTQytTCwUjAwNLBZIBA6OnLz8DA0MLIwND'
                'xZy9U7z9DzkIHF/ue5C9zeTjos52OVvFCQIWXZ2dMi7MbRWxb5zMXmrXalR8'
                'WvzT8I9FXuL2HHPeWo85KZfOvfnz7/K5vNssDI85FvitP34l9EZU79GuB4U2'
                'RxM95qQGMPPqRfyb/YvnJ8tZXRvnsBZmj57n7ucO1UZWn7y0ONtNTE45WmeZ'
                'Wd8by2/Ny1nZb34yjkzM9rIzXNI73feDNWfHa4N5L0/fXLJe2qt29pX6K3dl'
                'pvRYmrTUxNRz767SXfzPZ8X1SJuDB6U3bah0P16SMbddZm6xp3rf+7kCv9t8'
                '50hLr+2x3Han/8nfW5ZVWV7+rWHrpcxlxB5vEVnuuPvq29DHv6TzJhy+uqTy'
                'aOHuqy+/3ahZ9bHZ7vl3W3Pzie32RfGnEs9/X3lFva+zd1rFy90Tw2Pcp5d8'
                'mdLnKCNc7ftw56m4/69t/VTmWpgFdrDM7O1j//3dsbHo9wRT+2/1EhfP3+b0'
                '2DHtvK/t8vVe76UC3uwWsZx7r9Roh9LfLVxz3E6eXq37Papo3fXqVzs//tF3'
                'USuqBAART+Do')
        pipeline = cpp.Pipeline()
        def callback(caller,event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO.StringIO(zlib.decompress(base64.b64decode(data))))        
        self.assertEqual(len(pipeline.modules()), 1)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module, R.RescaleIntensity))
        self.assertFalse(module.wants_automatic_low.value)
        self.assertTrue(module.wants_automatic_high.value)
        self.assertAlmostEqual(module.source_low.value, .5)
    
    def test_01_04_load_matlab_enter_manual(self):
        '''Load a pipeline with manual low and high scaling'''
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUXAuSk0s'
                'SU1RyM+zUnArylTwKs1RMDQAIitTYytTAwUjAwNLBZIBA6OnLz8DA0MLIwND'
                'xZy9U856HXYQOK6uuFZ+qtCHRQ8U3f236k65NpujyTZi6dRHpdnbUhVvttSs'
                '+Ppk8U8Ju77ZZeZ3dRZ6JhcmeKSV1f33TDPPZGooZQhIv+78zGrN2mPJvp9U'
                '5j3QUCoRvHagwXje/zQ7V0ZHY3b/icKPBYKEfyrOrT7vbR9b9eHNjYPKT04d'
                'PeO20fqw4w8LcYX4OiX5GzMn+PNECqcm/3FzehR4rrjWdPa3r0pL8yf/7N83'
                's3macXvbFP9X+QnB+U+uzPf4qtZ/3KLGlW9b/s0Z39YWxy8oXvVC5aNsb0HC'
                'zpa4nS8Oz0o8Xu1/f33sguXpX0oySrWKrj+1UD4seSGvtPrqjn9d0iIFpqlx'
                'nnfySnfZ2s3P+rNA/0fueV2fZw/770zfdv9z7ZovnkmPFrHGscS9mX7dUFTW'
                'eHGyYFbyfk3b6+uu/6/qV3ZV78wVUfRMW/r48LfaCwnba0/Mlv9vz3Pzua+z'
                'kO7V4mD9F6s372ab8lsv9VxK+VyZdT72i5nSDT79STq7943F9dO6Xw+5/BPf'
                'nF4UBQBPz9+M')
        pipeline = cpp.Pipeline()
        def callback(caller,event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO.StringIO(zlib.decompress(base64.b64decode(data))))        
        self.assertEqual(len(pipeline.modules()), 1)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module, R.RescaleIntensity))
        self.assertFalse(module.wants_automatic_low.value)
        self.assertFalse(module.wants_automatic_high.value)
        self.assertAlmostEqual(module.source_scale.min, .1)
        self.assertAlmostEqual(module.source_scale.max, .9)

    def test_01_05_load_matlab_greater_than_one(self):
        '''Load a pipeline, dividing by the minimum'''
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUXAuSk0s'
                'SU1RyM+zUnArylTwKs1RMDQAIitTMysTSwUjAwNLBZIBA6OnLz8DA0M1IwND'
                'xZy9U876HXIQOL7c9yA/z8OOTva+eRwTBD6k7ZHgW8TovEev7IDvqW2Z291s'
                'fmbYNfU/0XtzaWnmAtfDKpPf+Tz/Pv9tyW0thiv+DKceVWndads6NSRHUu+x'
                'YZHfTRutRubSqf/F7BQVVYP51Y90Gzb1vvzTcPbP89QNO78+2L2x3XmTQXcr'
                '7+OjIodfFC5zLP3dWbfAfNl8jtvLTrv98FN+ZXxU+29J2eXrz1fuC31oX2bE'
                'rp3MJ6qs/zpfcWW50Sv9nl+zutwl9grx37U2XJb8+kqQ1aX3zioyh9nqldc8'
                'NJ5itdbW6tu0Pt6z33bVJ75Tk3+eU8i3Zdbcd4kx+Ue/fi9YemVOyp2sbdax'
                'ps8P/6jz/7z729qzTx7235n+df/zXzZX3Y+VOD6z4P9rcWL95FI54blsqXps'
                'ocnxruuPV/VtntLXE3uoU3HzJc6E79UbFtyoPjFr/i99Hgl3scB9PvNnf5q3'
                'b1tEqML98swi041Z6QWVvyzZC/oU9Ndfu+N9cGfc+xXXl33er5ZeqAwAZ7jf'
                'Pg==')
        pipeline = cpp.Pipeline()
        def callback(caller,event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO.StringIO(zlib.decompress(base64.b64decode(data))))
        self.assertEqual(len(pipeline.modules()), 1)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module, R.RescaleIntensity))
        self.assertEqual(module.rescale_method.value, 
                         R.M_DIVIDE_BY_IMAGE_MINIMUM)
    
    def test_01_06_load_matlab_match(self):
        '''Load a pipeline, matching to another image'''
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUXAuSk0s'
                'SU1RyM+zUnArylTwKs1RMDRQMDS0MjCwMjRTMDIwsFQgGTAwevryMzAwTGFk'
                'YKiYs3eKt/8hB4Hjy30PsntVXTnC7O7P4sFRoXzPgoGN5+OuCwvzLoX/Mnhw'
                'sv/Z8Q+Pd2jvvpAndauoYJKv9eWff9OtN+cKM0SJM5SW7U3xbt97tWX9UrHv'
                '4hLHr2xeLCVRoP7ofo6up8fJUwdVC4V6HiQY2X0z+/daz8Jm1o+wRw+m7HiZ'
                'knb5SGyixFkzIZH++Bdic1n/upyY5TP7MXvviveccS9WX3SOtQ97ZXbz18X+'
                '2gtFvy54HK38J9D3082vLuq4yD+dJd+MswWfu7P+6T1UXN93cZZFRiHvzn6l'
                'udGu7b+FhdbfjxbetDTvEddcv8a+eRcvLrxrO7la67ik5LkGv93X7fulv5w+'
                's3rZl87fc8u2X28v+nzueTvzyX6uH3sszxY2K1ZlizDrV9VnZsoK3Jke9rZG'
                '/O33qJWHa18JSb+94N/0yWrZouS0kqgrmw0yln0L/for/n3h0hcF95UMPU/+'
                'eclSUMUnFTLbOe7/kfqkN0dfuJrcW/l8WVxAeHo5r8b3ucssJ98tLd5h9LXH'
                '2KJ54nf+6ndrk+Ll/Z94T/4YH9ldfBAAEkrtMg==')
        pipeline = cpp.Pipeline()
        def callback(caller,event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO.StringIO(zlib.decompress(base64.b64decode(data))))
        self.assertEqual(len(pipeline.modules()), 1)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module, R.RescaleIntensity))
        self.assertEqual(module.image_name.value, "OrigBlue")
        self.assertEqual(module.rescaled_image_name.value, "RescaledBlue")
        self.assertEqual(module.rescale_method, R.M_SCALE_BY_IMAGE_MAXIMUM)
        self.assertEqual(module.matching_image_name, "ReferenceBlue")
    
    def test_01_07_load_matlab_convert(self):
        '''Load a matlab pipeline with convert to 8-bit'''
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUXAuSk0s'
                'SU1RyM+zUnArylTwKs1RMDRQMDS0MjC2MjJQMDIwsFQgGTAwevryMzAw1DAy'
                'MFTM2TvlfPYhA5Hj8d6l9jKPLh7ks32notXxzmzb5PadC53LerOnOPh6zT51'
                'J7P+1r+Wv57eJhclurbl/Xhwcc/17z/3fTHNFWV4lc6QWmgr/u7QLS+tMp7p'
                'HzmK/V7oaDayl079L2bnZug4WaA/cMYjFrNln2utUtefzih+3cma2cGekSfG'
                'Lb3kM2ff5Ocr2a6+Ff/UeFjw55EN2btyOsRVFHu04l7evukbf2ztvtCH9u/K'
                '+PyOyWi5xV27f3jbvdMr9hu9ytaSe/REttWiQiDZaqvf2UsT/514wXT8zvMz'
                '738KH1rq97mhb/fix06Lt76Ln7H79PFK6znsZ912F8tcjy3cyxxzctbkntm9'
                'YbsXP6uRuf86q+7+vq0zbf5M/F3073tMfFRtis+zjLZ0Q+/Ff6winxeufiws'
                '9WBF1pvVL76GnC9MfHnCwkFG0kh7Lse3/ezsXXvb1/xc+d9pfpGP8KHp33Zq'
                'yr943RXK+ql2ulq48OowtunL55ezPOf89Cvt7F7ROa/fzqvKtfrPHSxacBwA'
                '5zLjFA==')
        pipeline = cpp.Pipeline()
        def callback(caller,event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO.StringIO(zlib.decompress(base64.b64decode(data))))
        self.assertEqual(len(pipeline.modules()), 1)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module, R.RescaleIntensity))
        self.assertEqual(module.rescale_method, R.M_CONVERT_TO_8_BIT)
                
    def test_01_08_load_matlab_measurement(self):
        data = ('eJzzdQzxcXRSMNUzUPB1DNFNy8xJ1VEIyEksScsvyrVSCHAO9/TTUXAuSk0s'
                'SU1RyM+zUnArylTwKs1RMDRQMDS0MjCzMjBUMDIwsFQgGTAwevryMzAwLGJk'
                'YKiYs3eKb/YhB4E2dbNb/N0VmlsuOL9YuXxBU0a11lJ224zuri9h19KmtM5o'
                'SRF9u9J+rf3a3WWLT5rNkPBiN5s988xnP6PJS5gY5iY3CN33/6F1oF906XrX'
                'aR/aT0iUpjkKluyY8lF/37Ejy1OSHs+4wc2TkJ2457XP3Yu3bse92nnt0DG7'
                'me6Td34V/8z56+BnE5anT8V3OVV72As8ElvGW+DJ/Mpq0vRfWSXR11O97nZZ'
                'yLz9tUD1y0KZzu4/7Deevub8+Xzin1Vf2CX2CEuvdb+3bP+1St+LOwNLWuwP'
                'ie42n/diUlSGz7W2t0Lcus0fN2wU2WxSfj7a+6L+kS/cCdeKi8pvWtgeexlg'
                'LH22Jib78NbgHYsu2T+8fqZqsebvyf35253q7te2iz11LJo7ZZc4l/ofOaMk'
                'Qbd7u4qNnA3/H/i69N7yb9vvH5wZFP8jZMrcn+8OnV4XHFqyylC22UqsauqJ'
                'Wtld/68Xz9GyOiS+ueNETonNDXt2Xr7ZzkH/n9QveW1QwnTq2qvqCK+V0Q/S'
                'U0982+u2U8t+tXpB5KuXlhZzJ4df3/9/cuSvqt3q9lsM/vH2PK4vBwDa3/W+')
        pipeline = cpp.Pipeline()
        def callback(caller,event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO.StringIO(zlib.decompress(base64.b64decode(data))))
        self.assertEqual(len(pipeline.modules()), 1)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module, R.RescaleIntensity))
        self.assertEqual(module.rescale_method, R.M_DIVIDE_BY_MEASUREMENT)
        self.assertEqual(module.divisor_measurement, "Metadata_ImageDivisor")
    
    def test_01_09_load_v1(self):
        data = ('eJztWl9P2zAQd2lhMKSNaRKbtBc/7AE2GqXlj6CaoB3dtG6UVYA2IcSYaV3w'
                '5MRV4rB2ExIfa498pH2ExW3SpKYlbSm0aIlkNXfx737ns++SOM1n9rYyb+Gy'
                'osJ8Zi9eJhTDAkW8zAwtBXW+ADcNjDguQaan4HuDwI8WhQkVJpKpxZWUugyT'
                'qroG+jsiufwj8fsSgAn7Z9JuY86lcUeO+JqQdzHnRD8xx0EMPHf0l3b7ggyC'
                'jin+gqiFTY/C1ef0MturVZqX8qxkUbyNNH9n+9i2tGNsmJ/LLtC5XCBVTHfJ'
                'LywNwe22g8+ISZju4B37srbJy7jEK+JwOePFISLFIWq3WZ9e9P8AvP6xNnF7'
                '4us/48hEL5EzUrIQhURDJ00vhD01wF60xV4UZLczN8KlA3Azkv+i7eEqj7+r'
                'oiKHGuLF0274x1rsjIFtBrrin5b4hbyDzSKiuCTG0G3cIi12ImCxS1ysBRez'
                '/daxwJ0G4JYkv4W8ecqYiaFZwUVSJkV4Vs8TyBk8xtDAJubiHMGiZXKmQQPp'
                'J9gdX1CcHkp8Qs4yqDMOLdNJGHm8E5Id93DtTIH2uF7mdxC4u/AzKI+fgdb4'
                'CjmLy8iiHOZEEsMsMXCRM6N2q/7LeayoiYHxDdJPOW9UZW2tn/Ht29XxJn6u'
                'BvA9AK3zKmRVSSzY/vY1H8PxN2n7uzqUfAvKm6eSv0LebRQ6p8zVq2DT3uiv'
                'Y3V5UPfpUYlzN/fLRBvcLdeLruLc6f7cr5/pAL4p0BpnIW/WOKtQZGo+OxcB'
                'dj5JdoT8bW6j8EY8+ON15fX8kZC+Ykp32M/1g0y8cDjvajYZtTR9/UCNrx3+'
                'Tiwkzxudd4mNrCvn28Z9kPMlr4+kgwt6LlqVxi1k4fs+RoYzoKXz+bhQ5ZnO'
                'Tx1d0tFlUc3T3GR8hQA/X0h+Cjmnc6ybhNeO8hjpntTpOfSu69cw1vmo1etO'
                '63LU/Bx03eoXdxHg532qU73g7kud6hc3+bi3fYzbqiPt3kvrmx4nBrMqg7cz'
                'anW03f6J5zckeglXbpO/3f4JO/5hv6l6gRt2fQxxIS7Ehbj/EZf24YZx/whx'
                'dzufo/ocE+JGA5cG16+fsB6EuBDXO64a6fw+LGT/fr3o/x1cn4evQGseCrmI'
                'Ka0YTPx/w1C0+p8MTIUyVGp85Ve27NOc74O/4KkE8KQlnnQnHg0j0zJwnYq4'
                'W5NKvqGtszY3LLvZ/1iReFc68RqNj/EepfN1vsl2dd6m2vD54z9mS7PRmWvn'
                'W55nb/7/bvTDF41Ernx/mw7AxXw+iUPg/4De1tncNf3dMd5V/38aZ6rY')
        pipeline = cpp.Pipeline()
        def callback(caller,event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO.StringIO(zlib.decompress(base64.b64decode(data))))
        self.assertEqual(len(pipeline.modules()), 3)
        module = pipeline.modules()[2]
        self.assertTrue(isinstance(module, R.RescaleIntensity))
        #
        # image_name = DNA
        # rescaled_image_name = RescaledDNA
        # rescaling_method = M_MANUAL_IO_RANGE
        # manual intensities
        # source_low = .01
        # source_high = .99
        # src_scale = .1 to .9
        # dest_scale = .2 to .8
        # low_truncation_choice = R_SET_TO_CUSTOM
        # custom_low_truncation = .05
        # high_truncation_choice = R_SET_TO_CUSTOM
        # custom_high_truncation = .95
        # matching_image_name = Cytoplasm
        # divisor_value = 2
        # divisor_measurement = Intensity_MeanIntensity_DNA
        self.assertEqual(module.image_name.value, "DNA")
        self.assertEqual(module.rescaled_image_name.value, "RescaledDNA")
        self.assertEqual(module.rescale_method.value, R.M_MANUAL_IO_RANGE)
        self.assertFalse(module.wants_automatic_high.value)
        self.assertFalse(module.wants_automatic_low.value)
        self.assertAlmostEqual(module.source_low.value, .01)
        self.assertAlmostEqual(module.source_high.value, .99)
        self.assertAlmostEqual(module.source_scale.min, .1)
        self.assertAlmostEqual(module.source_scale.max, .9)
        self.assertEqual(module.low_truncation_choice.value, R.R_SET_TO_CUSTOM)
        self.assertEqual(module.high_truncation_choice.value, R.R_SET_TO_CUSTOM)
        self.assertAlmostEqual(module.custom_low_truncation.value, .05)
        self.assertAlmostEqual(module.custom_high_truncation.value, .95)
        self.assertEqual(module.matching_image_name.value, "Cytoplasm")
        self.assertAlmostEqual(module.divisor_value.value, 2)
        self.assertEqual(module.divisor_measurement.value, "Intensity_MeanIntensity_DNA")
    
    def make_workspace(self, input_image, input_mask = None,
                       reference_image=None, reference_mask = None,
                       measurement=None):
        pipeline = cpp.Pipeline()
        object_set = cpo.ObjectSet()
        image_set_list = cpi.ImageSetList()
        image_set = image_set_list.get_image_set(0)
        measurements = cpmeas.Measurements() 
        module = R.RescaleIntensity()
        module.image_name.value = INPUT_NAME
        if input_mask is None:
            image = cpi.Image(input_image)
        else:
            image = cpi.Image(input_image, input_mask)
        image_set.add(INPUT_NAME, image)
        module.rescaled_image_name.value = OUTPUT_NAME
        if reference_image is not None:
            module.matching_image_name.value = REFERENCE_NAME
            if reference_mask is None:
                image = cpi.Image(reference_image)
            else:
                image = cpi.Image(reference_image, mask = reference_mask)
            image_set.add(REFERENCE_NAME, image)
        if measurement is not None:
            module.divisor_measurement.value = MEASUREMENT_NAME
            measurements.add_image_measurement(MEASUREMENT_NAME, measurement)
        workspace = cpw.Workspace(pipeline,
                                  module,
                                  image_set,
                                  object_set,
                                  measurements,
                                  image_set_list)
        return workspace,module
        
    def test_03_01_stretch(self):
        np.random.seed(0)
        expected = np.random.uniform(size=(10,10))
        expected[0,0] = 1
        expected[9,9] = 0
        workspace, module = self.make_workspace(expected / 2 + .1)
        module.rescale_method.value = R.M_STRETCH
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps))
    
    def test_03_02_stretch_mask(self):
        np.random.seed(0)
        expected = np.random.uniform(size=(10,10))
        expected[0,0] = 1
        expected[9,9] = 0
        mask = np.ones(expected.shape, bool)
        mask[3:5,4:7] = False
        expected[~ mask] = 1.5
        workspace, module = self.make_workspace(expected / 2 + .1,mask)
        module.rescale_method.value = R.M_STRETCH
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels[mask] - expected[mask]) <=
                               np.finfo(float).eps))
    
    def test_04_01_manual_input_range(self):
        np.random.seed(0)
        expected = np.random.uniform(size=(10,10))
        workspace, module = self.make_workspace(expected / 2 + .1)
        module.rescale_method.value = R.M_MANUAL_INPUT_RANGE
        module.wants_automatic_low.value = False
        module.wants_automatic_high.value = False
        module.source_scale.min = .1
        module.source_scale.max = .6
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps))
    
    def test_04_02_manual_input_range_auto_low(self):
        np.random.seed(0)
        expected = np.random.uniform(size=(10,10))
        expected[0,0] = 0
        workspace, module = self.make_workspace(expected / 2 + .1)
        module.rescale_method.value = R.M_MANUAL_INPUT_RANGE
        module.wants_automatic_low.value = True
        module.wants_automatic_high.value = False
        module.source_high.value = .6
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps))

    def test_04_03_manual_input_range_auto_high(self):
        np.random.seed(0)
        expected = np.random.uniform(size=(10,10))
        expected[0,0] = 1
        workspace, module = self.make_workspace(expected / 2 + .1)
        module.rescale_method.value = R.M_MANUAL_INPUT_RANGE
        module.wants_automatic_low.value = False
        module.wants_automatic_high.value = True
        module.source_low.value = .1
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps))
        
    def test_04_03_manual_input_range_mask(self):
        np.random.seed(0)
        expected = np.random.uniform(size=(10,10))
        expected[0,0] = 1
        mask = np.ones(expected.shape, bool)
        mask[3:5,4:7] = False
        expected[~ mask] = 1.5
        workspace, module = self.make_workspace(expected / 2 + .1,mask)
        module.rescale_method.value = R.M_MANUAL_INPUT_RANGE
        module.wants_automatic_low.value = False
        module.wants_automatic_high.value = True
        module.source_low.value = .1
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels[mask] - expected[mask]) <=
                               np.finfo(float).eps))
    
    def test_04_03_manual_input_range_truncate(self):
        np.random.seed(0)
        expected = np.random.uniform(size=(10,10))
        expected_low_mask = np.zeros(expected.shape, bool)
        expected_low_mask[2:4,1:3] = True
        expected[expected_low_mask] = -.05
        expected_high_mask = np.zeros(expected.shape, bool)
        expected_high_mask[6:8,5:7] = True
        expected[expected_high_mask] = 1.05
        mask = ~(expected_low_mask | expected_high_mask)
        for low_truncate_method in (R.R_MASK, R.R_SCALE, R.R_SET_TO_CUSTOM, 
                                    R.R_SET_TO_ZERO):
            for high_truncate_method in (R.R_MASK, R.R_SCALE, R.R_SET_TO_CUSTOM,
                                         R.R_SET_TO_ONE):
                workspace, module = self.make_workspace(expected / 2 + .1)
                module.rescale_method.value = R.M_MANUAL_INPUT_RANGE
                module.wants_automatic_low.value = False
                module.wants_automatic_high.value = False
                module.source_scale.min = .1
                module.source_scale.max = .6
                module.low_truncation_choice.value = low_truncate_method
                module.high_truncation_choice.value = high_truncate_method
                module.custom_low_truncation.value = -1
                module.custom_high_truncation.value = 2
                module.run(workspace)
                image = workspace.image_set.get_image(OUTPUT_NAME)
                pixels = image.pixel_data
                self.assertTrue(np.all(np.abs(pixels[mask] - expected[mask]) <=
                                       np.finfo(float).eps),
                                "Failed with low method=%s, high method=%s"%
                                (low_truncate_method, high_truncate_method))
                if low_truncate_method == R.R_MASK:
                    self.assertTrue(image.has_mask)
                    self.assertTrue(np.all(image.mask[expected_low_mask] == False))
                    if high_truncate_method != R.R_MASK:
                        self.assertTrue(np.all(image.mask[expected_high_mask]))
                else:
                    if low_truncate_method == R.R_SCALE:
                        low_value = -.05
                    elif low_truncate_method == R.R_SET_TO_CUSTOM:
                        low_value = -1
                    elif low_truncate_method == R.R_SET_TO_ZERO:
                        low_value = 0
                    self.assertTrue(np.all(np.abs(pixels[expected_low_mask] - low_value) <= np.finfo(float).eps),
                                    "Low method (%s) failed"%low_truncate_method)
                if high_truncate_method == R.R_MASK:
                    self.assertTrue(image.has_mask)
                    self.assertTrue(np.all(image.mask[expected_high_mask] == False))
                else:
                    if high_truncate_method == R.R_SCALE:
                        high_value = 1.05
                    elif high_truncate_method == R.R_SET_TO_CUSTOM:
                        high_value = 2
                    elif high_truncate_method == R.R_SET_TO_ONE:
                        high_value = 1
                    self.assertTrue(np.all(np.abs(pixels[expected_high_mask] - high_value) <= np.finfo(float).eps),
                                    "High truncate method (%s) failed"%high_truncate_method)
                
    def test_05_01_manual_io_range(self):
        np.random.seed(0)
        expected = np.random.uniform(size=(10,10))
        workspace, module = self.make_workspace(expected / 2 + .1)
        expected = expected * .75 + .05
        module.rescale_method.value = R.M_MANUAL_IO_RANGE
        module.wants_automatic_low.value = False
        module.wants_automatic_high.value = False
        module.source_scale.min = .1
        module.source_scale.max = .6
        module.dest_scale.min = .05
        module.dest_scale.max = .80
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps))
    
    def test_06_01_divide_by_image_minimum(self):
        np.random.seed(0)
        image = np.random.uniform(size=(10,10))
        image[0,0] = 0
        image = image / 2 + .1
        expected = image * 10
        workspace, module = self.make_workspace(image)
        module.rescale_method.value = R.M_DIVIDE_BY_IMAGE_MINIMUM
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps * 10))

    def test_06_02_divide_by_image_minimum_masked(self):
        np.random.seed(0)
        image = np.random.uniform(size=(10,10))
        image[0,0] = 0
        image = image / 2 + .1
        mask = np.ones(image.shape,bool)
        mask[3:6,7:9] = False
        image[~mask] = .05
        expected = image * 10
        workspace, module = self.make_workspace(image, mask)
        module.rescale_method.value = R.M_DIVIDE_BY_IMAGE_MINIMUM
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels[mask] - expected[mask]) <= np.finfo(float).eps * 10))

    def test_07_01_divide_by_image_maximum(self):
        np.random.seed(0)
        image = np.random.uniform(size=(10,10))
        image = image / 2 + .1
        image[0,0] = .8
        expected = image / .8
        workspace, module = self.make_workspace(image)
        module.rescale_method.value = R.M_DIVIDE_BY_IMAGE_MAXIMUM
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps))

    def test_07_02_divide_by_image_minimum_masked(self):
        np.random.seed(0)
        image = np.random.uniform(size=(10,10))
        image = image / 2 + .1
        image[0,0] = .8
        mask = np.ones(image.shape,bool)
        mask[3:6,7:9] = False
        image[~mask] = .9
        expected = image / .8
        workspace, module = self.make_workspace(image, mask)
        module.rescale_method.value = R.M_DIVIDE_BY_IMAGE_MAXIMUM
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels[mask] - expected[mask]) <= np.finfo(float).eps ))

    def test_08_01_divide_by_value(self):
        np.random.seed(0)
        image = np.random.uniform(size=(10,10))
        image = image / 2 + .1
        value = .9
        expected = image / value
        workspace, module = self.make_workspace(image)
        module.rescale_method.value = R.M_DIVIDE_BY_VALUE
        module.divisor_value.value = value
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps))
    
    def test_09_01_divide_by_measurement(self):
        np.random.seed(0)
        image = np.random.uniform(size=(10,10))
        image = image / 2 + .1
        value = .75
        expected = image / value
        workspace, module = self.make_workspace(image, measurement=value)
        module.rescale_method.value = R.M_DIVIDE_BY_MEASUREMENT
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps))
    
    def test_10_01_scale_by_image_maximum(self):
        np.random.seed(0)
        image = np.random.uniform(size=(10,10))
        image[0,0] = 1
        image = image / 2 + .1
        reference = np.random.uniform(size=(10,10)) * .75
        reference[0,0] = .75
        expected = image * .75 / .60
        workspace, module = self.make_workspace(image, 
                                                reference_image = reference)
        module.rescale_method.value = R.M_SCALE_BY_IMAGE_MAXIMUM
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps))

    def test_10_02_scale_by_image_maximum_mask(self):
        np.random.seed(0)
        image = np.random.uniform(size=(10,10))
        image[0,0] = 1
        image = image / 2 + .1
        mask = np.ones(image.shape, bool)
        mask[3:6,4:8] = False
        image[~mask] = .9
        reference = np.random.uniform(size=(10,10)) * .75
        reference[0,0] = .75
        rmask = np.ones(reference.shape, bool)
        rmask[7:9,1:3] = False
        reference[~rmask] = .91
        expected = image * .75 / .60
        workspace, module = self.make_workspace(image,
                                                input_mask = mask,
                                                reference_image = reference,
                                                reference_mask = rmask)
        module.rescale_method.value = R.M_SCALE_BY_IMAGE_MAXIMUM
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels[mask] - expected[mask]) <= np.finfo(float).eps))
    
    def test_11_01_convert_to_8_bit(self):
        np.random.seed(0)
        image = np.random.uniform(size=(10,10))
        expected = (image * 255).astype(np.uint8)
        workspace, module = self.make_workspace(image)
        module.rescale_method.value = R.M_CONVERT_TO_8_BIT
        module.run(workspace)
        pixels = workspace.image_set.get_image(OUTPUT_NAME).pixel_data
        self.assertTrue(np.all(np.abs(pixels - expected) <= np.finfo(float).eps))
