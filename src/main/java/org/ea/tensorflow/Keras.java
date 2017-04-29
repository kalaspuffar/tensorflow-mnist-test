package org.ea.tensorflow;

import org.tensorflow.*;
import java.util.Arrays;
import java.nio.file.*;
import java.nio.*;
import java.util.*;
/**
 * Hello world!
 *
 */
public class Keras
{
    public static void main( String[] args )
    {
      System.out.println( "Hello World! I'm using tensorflow version " + TensorFlow.version() );

      try {
        MnistReader mrTest = new MnistReader("mnist/t10k-labels-idx1-ubyte", "mnist/t10k-images-idx3-ubyte");

        SavedModelBundle smb = SavedModelBundle.load("./model_keras", "serve");
        Session s = smb.session();

        int correct_prediction = 0;
        for(int i=0; i<mrTest.size(); i++) {

          FloatBuffer fb = FloatBuffer.allocate(784);
          byte[] imgData = mrTest.readNextImage();
          for(byte b : imgData) {
              fb.put((float)(b & 0xFF)/255.0f);
          }
          fb.rewind();

          float[] keep_prob_arr = new float[1024];
          Arrays.fill(keep_prob_arr, 1f);

          Tensor inputTensor = Tensor.create(new long[] {784}, fb);
          Tensor keep_prob = Tensor.create(Boolean.FALSE);

          Tensor result = s.runner()
            .feed("input_tensor", inputTensor)
            .feed("dropout/keras_learning_phase", keep_prob)
            .fetch("output_tensor")
            .run().get(0);

          float[][] m = new float[1][10];
          //m[0] = new float[10];
          //Arrays.fill(m[0], 0);

          float[][] matrix = result.copyTo(m);
          float maxVal = 0;
          int inc = 0;
          int predict = -1;
          for(float val : matrix[0]) {
            if(val > maxVal) {
              predict = inc;
              maxVal = val;
            }
            inc++;
          }
          if(predict == mrTest.readNextLabel()) {
            correct_prediction++;
          }
        }
        System.out.println("We have "+correct_prediction+"/10000 which is "+((float)correct_prediction/100f)+"%");
      } catch (Exception e) {
        e.printStackTrace();
      }
    }
}
