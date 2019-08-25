package net.haesleinhuepf.clijpy;

import ij.ImagePlus;
import net.haesleinhuepf.clij.CLIJ;
import net.haesleinhuepf.clij.clearcl.ClearCLBuffer;
import net.haesleinhuepf.clij.coremem.enums.NativeTypeEnum;
import net.haesleinhuepf.clij2.CLIJ2;
import net.haesleinhuepf.clij2.utilities.CLIJ2Ops;
import net.imglib2.RandomAccessibleInterval;

/**
 * The CLIJPY gateway.
 *
 * Author: haesleinhuepf
 *         August 2019
 */
public class CLIJPY {


    private static CLIJPY instance;
    private static CLIJ2 clij2;
    private final CLIJ clij;

    public final CLIJ2Ops op;

    public CLIJPY() {
        this.clij = CLIJ.getInstance();
        this.clij2 = new CLIJ2(clij);
        op = clij2.op;
    }

    private CLIJPY(CLIJ clij) {
        this.clij = clij;
        this.clij2 = new CLIJ2(clij);
        op = clij2.op;
    }

    public static CLIJPY getInstance() {
        if (instance == null) {
            instance = new CLIJPY(CLIJ.getInstance());
        }
        return instance;
    }

    public CLIJPY getInstance(String id) {
        if (instance == null) {
            instance = new CLIJPY(CLIJ.getInstance(id));
        }
        return instance;
    }

    public Object push(Object object) {
        if (object instanceof RandomAccessibleInterval) {
            return clij.push((RandomAccessibleInterval)object);
        }
        System.out.println("push object falied; not supported: " + object);
        return null;
    }

    public Object pull(ClearCLBuffer buffer) {
        return clij.pullRAI(buffer);
    }

    public ClearCLBuffer create(long[] dimensions, NativeTypeEnum type) {
        return clij.create(dimensions, type);
    }

    public ClearCLBuffer create(long[] dimensions) {
        return clij.create(dimensions, NativeTypeEnum.Float);
    }

    public ClearCLBuffer create(ClearCLBuffer buffer) {
        return clij.create(buffer);
    }

    /*
    * Deprecated: Use op without brackets instead
    */
    @Deprecated
    public CLIJ2Ops op() {
        return clij2.op;
    }

    public String getGPUName() {
        return clij.getGPUName();
    }

    public void show(Object object, String headline) {
        ImagePlus imp = clij.convert(object, ImagePlus.class);
        imp.setTitle(headline);
        imp.show();
    }
}
