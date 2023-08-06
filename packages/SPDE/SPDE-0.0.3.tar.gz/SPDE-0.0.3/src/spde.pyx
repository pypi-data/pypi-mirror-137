from libcpp cimport bool
from libcpp.vector cimport vector


cdef extern from "TurboOptimizer.hpp":


	cdef cppclass TurboOptimizer:
		TurboOptimizer(int nx ,int ny ,double dx ,double dy ,double x0 ,double y0 ,double scale ,double sill ,int param , int flagOne) except +
		int _nx,_ny,param
		vector[int] a
		double _dx,_dy,_x0,_y0,_scale,_sill
		vector[int] interpolate_rows(vector[double] x,vector[double]y)
		vector[int] interpolate_cols(vector[double] x,vector[double]y)
		vector[double] interpolate_values(vector[double] x,vector[double] y) 
		vector[int] getQ_rows() 
		vector[int] getQ_cols() 
		vector[double] getQ_values() 
		void run(bool verbose)
		void setModelByRange(double rangev, double sill, int param)

cdef class PyTurboOptimizer:
	cdef TurboOptimizer *thisptr
	def __cinit__(self,nx=[2,2],dx=[1.,1.] ,x0=[0.,0.] ,rangev=1. ,sill=1. ,param=1 ):
		self.thisptr = new TurboOptimizer(nx[0],nx[1],dx[0],dx[1],x0[0],x0[1],rangev,sill,param,0)
		self.thisptr.setModelByRange(rangev,sill,param)
		self.thisptr.run(0)
	def __dealloc__(self):
		del self.thisptr
	def get_Q(self):
		return [self.thisptr.getQ_rows(),self.thisptr.getQ_cols(),self.thisptr.getQ_values()]
	def get_Aproj(self,X):
		return [self.thisptr.interpolate_rows(X[:,0],X[:,1]),self.thisptr.interpolate_cols(X[:,0],X[:,1]),self.thisptr.interpolate_values(X[:,0],X[:,1])]

        
        
