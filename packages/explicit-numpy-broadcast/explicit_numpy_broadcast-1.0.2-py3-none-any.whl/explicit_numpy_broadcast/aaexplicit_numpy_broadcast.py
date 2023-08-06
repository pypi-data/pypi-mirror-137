import numpy as np
from IPython.core.display import display, HTML, Markdown


class ExplicitArray(np.ndarray):
    def __array_ufunc__(self, ufunc, method, *inputs, out=None, **kwargs):
        args = []
        in_no = []
        for i, input_ in enumerate(inputs):
            if isinstance(input_, ExplicitArray):
                in_no.append(i)
                args.append(input_.view(np.ndarray))
            else:
                args.append(input_)

        outputs = out
        out_no = []
        if outputs:
            out_args = []
            for j, output in enumerate(outputs):
                if isinstance(output, ExplicitArray):
                    out_no.append(j)
                    out_args.append(output.view(np.ndarray))
                else:
                    out_args.append(output)
            kwargs['out'] = tuple(out_args)
        else:
            outputs = (None,) * ufunc.nout

        info = {}
        if in_no:
            info['inputs'] = in_no
        if out_no:
            info['outputs'] = out_no

        results = super().__array_ufunc__(ufunc, method, *args, **kwargs)
        if results is NotImplemented:
            return NotImplemented

        if method == 'at':
            if isinstance(inputs[0], ExplicitArray):
                inputs[0].info = info
            return

        if ufunc.nout == 1:
            results = (results,)

        results = tuple((np.asarray(result).view(ExplicitArray)
                         if output is None else output)
                        for result, output in zip(results, outputs))
        if results and isinstance(results[0], ExplicitArray):
            results[0].info = info
        #
        # the above code is from the numpy doc at
        # https://numpy.org/doc/stable/user/basics.subclassing.html#array-ufunc-for-ufuncs
        #
        operation = None
        if ufunc == np.add:
            operation = "+"
        elif ufunc == np.subtract:
            operation = "-"
        elif ufunc == np.multiply:
            operation = "*"
        elif ufunc == np.matmul:
            operation = "@"
        tr_template = """
        <tr style='background-color:white;'>
            <td style='text-align:center;'>
                <span style='background-color:#def'>{1}</span>
            </td>
            <td></td>
            <td style='text-align:center;'>
                <span style='background-color:#edf'>{4}</span>
            </td>
            <td></td>
            <td style='text-align:center;'>
                <span style='background-color:#efd'>{7}</span>
            </td>
        </tr>
        <tr style='background-color:white;'>
            <td>
                <code style='display:inline-block; text-align:left; background-color:#def;'>
{0}
                </code>
            </td>
            <td style='font-size:200%; text-align: left;'>
            {2}
            </td>
            <td>
                <code style='display:inline-block; text-align:left; background-color:#edf;'>
{3}
                </code>
            </td>
            <td style='font-size:200%; text-align: left;'>
            {5}
            </td>
            <td>
                <code style='display:inline-block; text-align:left; background-color:#efd;'>
{6}
                </code>
            </td>
        </tr>"""
        th_template = "<tr style='background-color:#f5f5f5'><th style='text-align:left;' colspan=99>%s</th></tr>"
        if operation in ["+", "-", "*"]:
            a = inputs[0]
            b = inputs[1]
            aa, bb = np.broadcast_arrays(a, b)
            strings = [
                "<table style='font-size:10px'>",
                th_template % "Requested operation:",
                tr_template.format(
                    np.array2string(a), "shape "+str(a.shape),
                    operation,
                    np.array2string(b), "shape "+str(b.shape),
                    "=",
                    np.array2string(ufunc(a.view(np.ndarray), b.view(np.ndarray))),
                    "shape "+str(ufunc(a.view(np.ndarray), b.view(np.ndarray)).shape)
                ),
            ]
            if a.shape != aa.shape or b.shape != bb.shape:
                strings = strings + [
                    th_template % "This is because arrays were automatically broadcasted as follows:",
                    tr_template.format(
                        np.array2string(aa), "shape "+str(aa.shape),
                        operation,
                        np.array2string(bb), "shape "+str(bb.shape),
                        "=",
                        np.array2string(ufunc(aa.view(np.ndarray), bb.view(np.ndarray))),
                        "shape "+str(ufunc(aa.view(np.ndarray), bb.view(np.ndarray)).shape)
                    ),
                ]
            strings.append("</table>")
            display(HTML("".join(strings)))
        if operation == "@":
            a = inputs[0]
            b = inputs[1]
            strings = [
                "<table style='font-size:10px'>",
                th_template % "Requested matrix operation:",
                tr_template.format(
                    np.array2string(a), "shape "+str(a.shape),
                    operation,
                    np.array2string(b), "shape "+str(b.shape),
                    "=",
                    np.array2string(ufunc(a.view(np.ndarray), b.view(np.ndarray))),
                    "shape "+str(ufunc(a.view(np.ndarray), b.view(np.ndarray)).shape)
                ),
            ]
            if len(a.shape) + len(b.shape) >= 3: # don't do anything for 1d @ 1d
                if len(a.shape) == 1 or len(b.shape) == 1 or a.shape[:-2] != b.shape[:-2]:
                    strings.append(th_template % "Explanation:")
                if len(a.shape) == 1:
                    a = a[np.newaxis, ...]
                    strings.append(th_template % "Axis is prepended to first matrix: ({0},) -> (1, {0}):".format(inputs[0].shape[0]))
                    strings.append(tr_template.format(
                        np.array2string(a), "shape "+str(a.shape),
                        operation,
                        np.array2string(b), "shape "+str(b.shape),
                        "", "", ""
                    ))
                if len(b.shape) == 1:
                    b = b[..., np.newaxis]
                    strings.append(th_template % "Axis is appended to second matrix: ({0},) -> ({0},1):".format(inputs[1].shape[0]))
                    strings.append(tr_template.format(
                        np.array2string(a), "shape "+str(a.shape),
                        operation,
                        np.array2string(b), "shape "+str(b.shape),
                        "", "", ""
                    ))
                first_K_minus_2_dims = np.broadcast_shapes(a.shape[:-2], b.shape[:-2])
                a = np.broadcast_to(a, first_K_minus_2_dims + a.shape[-2:] )
                b = np.broadcast_to(b, first_K_minus_2_dims + b.shape[-2:])
                c = a.view(np.ndarray) @ b.view(np.ndarray)
                matrix_product_signature = str(a.shape[-2:])+", "+str(b.shape[-2:])+" → ("+str(a.shape[-2])+","+str(b.shape[-1])+")"
                if len(b.shape) > 2 or len(a.shape) > 2:
                    strings.append(th_template % "Matrix product %s on the last 2 axes with broadcasting on the first N-2 axes:" % matrix_product_signature)
                else:
                    strings.append(th_template % "Matrix product %s:" % matrix_product_signature )

                strings.append(tr_template.format(
                    np.array2string(a), "shape "+str(a.shape),
                    operation,
                    np.array2string(b), "shape "+str(b.shape),
                    "=", np.array2string(c), "shape "+str(c.shape)
                ))
                if len(inputs[0].shape) == 1:
                    c = np.squeeze(c, axis=-2)
                    strings.append(th_template % "Prepended axis is removed:")
                    strings.append(tr_template.format(
                        "", "", "", "", "", "",
                        np.array2string(c), "shape "+str(c.shape)
                    ))
                if len(inputs[1].shape) == 1:
                    c = np.squeeze(c, axis=-1)
                    strings.append(th_template % "Appended axis is removed:")
                    strings.append(tr_template.format(
                        "", "", "", "", "", "",
                        np.array2string(c), "shape "+str(c.shape)
                    ))
            strings.append("</table>")
            display(HTML("".join(strings)))

        return results[0] if len(results) == 1 else results



def explicit_array(a):
    return np.array(a).view(ExplicitArray)
