#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/include/builtins/None.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/min.hpp>
#include <pythonic/include/builtins/pythran/and_.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/gt.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/None.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/min.hpp>
#include <pythonic/builtins/pythran/and_.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/gt.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_mini_oper_modif_resol
{
  struct __transonic__
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type0>())) __type1;
      typedef typename pythonic::returnable<__type1>::type __type2;
      typedef __type2 result_type;
    }  ;
    inline
    typename type::result_type operator()() const;
    ;
  }  ;
  struct fill_field_fft_3d
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef __type0 __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::min{})>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef __type4 __type5;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type5>())) __type6;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type6>::type>::type __type7;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type9;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type9>::type>::type __type10;
      typedef decltype(std::declval<__type3>()(std::declval<__type7>(), std::declval<__type10>())) __type11;
      typedef typename pythonic::assignable<__type11>::type __type12;
      typedef __type12 __type13;
      typedef long __type14;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type13>(), std::declval<__type14>())) __type15;
      typedef decltype(pythonic::operator_::add(std::declval<__type15>(), std::declval<__type14>())) __type16;
      typedef decltype(std::declval<__type2>()(std::declval<__type16>())) __type17;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type17>::type::iterator>::value_type>::type __type18;
      typedef __type18 __type19;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type6>::type>::type __type20;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type9>::type>::type __type21;
      typedef decltype(std::declval<__type3>()(std::declval<__type20>(), std::declval<__type21>())) __type22;
      typedef typename pythonic::assignable<__type22>::type __type23;
      typedef __type23 __type24;
      typedef decltype(pythonic::operator_::functor::floordiv()(std::declval<__type24>(), std::declval<__type14>())) __type25;
      typedef decltype(pythonic::operator_::add(std::declval<__type25>(), std::declval<__type14>())) __type26;
      typedef decltype(std::declval<__type2>()(std::declval<__type26>())) __type27;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type27>::type::iterator>::value_type>::type __type28;
      typedef __type28 __type29;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type6>::type>::type __type30;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type9>::type>::type __type31;
      typedef decltype(std::declval<__type3>()(std::declval<__type30>(), std::declval<__type31>())) __type32;
      typedef typename pythonic::lazy<__type32>::type __type33;
      typedef __type33 __type34;
      typedef decltype(std::declval<__type2>()(std::declval<__type34>())) __type35;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type35>::type::iterator>::value_type>::type __type36;
      typedef __type36 __type37;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type19>(), std::declval<__type29>(), std::declval<__type37>())) __type38;
      typedef decltype(std::declval<__type1>()[std::declval<__type38>()]) __type39;
      typedef container<typename std::remove_reference<__type39>::type> __type40;
      typedef indexable<__type38> __type45;
      typedef decltype(pythonic::operator_::neg(std::declval<__type19>())) __type48;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type48>(), std::declval<__type29>(), std::declval<__type37>())) __type51;
      typedef decltype(std::declval<__type1>()[std::declval<__type51>()]) __type52;
      typedef container<typename std::remove_reference<__type52>::type> __type53;
      typedef indexable<__type51> __type59;
      typedef decltype(pythonic::operator_::neg(std::declval<__type29>())) __type64;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type48>(), std::declval<__type64>(), std::declval<__type37>())) __type66;
      typedef decltype(std::declval<__type1>()[std::declval<__type66>()]) __type67;
      typedef container<typename std::remove_reference<__type67>::type> __type68;
      typedef indexable<__type66> __type75;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type19>(), std::declval<__type64>(), std::declval<__type37>())) __type81;
      typedef decltype(std::declval<__type1>()[std::declval<__type81>()]) __type82;
      typedef container<typename std::remove_reference<__type82>::type> __type83;
      typedef indexable<__type81> __type89;
      typedef typename __combined<__type4,__type40,__type45,__type53,__type59,__type68,__type75,__type83,__type89>::type __type90;
      typedef __type39 __type91;
      typedef __type38 __type92;
      typedef pythonic::types::none_type __type93;
      typedef typename pythonic::returnable<__type93>::type __type94;
      typedef __type91 __ptype0;
      typedef __type92 __ptype1;
      typedef __type94 result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    inline
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& field_fft_in, argument_type1&& field_fft_out) const
    ;
  }  ;
  inline
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.12"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 >
  inline
  typename fill_field_fft_3d::type<argument_type0, argument_type1>::result_type fill_field_fft_3d::operator()(argument_type0&& field_fft_in, argument_type1&& field_fft_out) const
  {
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::min{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in))))>::type nk0_min = pythonic::builtins::functor::min{}(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in)));
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::min{}(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in))))>::type nk1_min = pythonic::builtins::functor::min{}(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in)));
    typename pythonic::lazy<decltype(pythonic::builtins::functor::min{}(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in))))>::type nk2_min = pythonic::builtins::functor::min{}(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_out)), std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_fft_in)));
    {
      long  __target139708402717312 = pythonic::operator_::add(pythonic::operator_::functor::floordiv()(nk0_min, 2L), 1L);
      for (long  ik0=0L; ik0 < __target139708402717312; ik0 += 1L)
      {
        {
          long  __target139708402717840 = pythonic::operator_::add(pythonic::operator_::functor::floordiv()(nk1_min, 2L), 1L);
          for (long  ik1=0L; ik1 < __target139708402717840; ik1 += 1L)
          {
            {
              long  __target139708401721296 = nk2_min;
              for (long  ik2=0L; ik2 < __target139708401721296; ik2 += 1L)
              {
                field_fft_out[pythonic::types::make_tuple(ik0, ik1, ik2)] = field_fft_in[pythonic::types::make_tuple(ik0, ik1, ik2)];
                if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::gt(ik0, 0L); }, [&] () { return pythonic::operator_::lt(ik0, pythonic::operator_::functor::floordiv()(nk0_min, 2L)); }))
                {
                  field_fft_out[pythonic::types::make_tuple(pythonic::operator_::neg(ik0), ik1, ik2)] = field_fft_in[pythonic::types::make_tuple(pythonic::operator_::neg(ik0), ik1, ik2)];
                  if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::gt(ik1, 0L); }, [&] () { return pythonic::operator_::lt(ik1, pythonic::operator_::functor::floordiv()(nk1_min, 2L)); }))
                  {
                    field_fft_out[pythonic::types::make_tuple(pythonic::operator_::neg(ik0), pythonic::operator_::neg(ik1), ik2)] = field_fft_in[pythonic::types::make_tuple(pythonic::operator_::neg(ik0), pythonic::operator_::neg(ik1), ik2)];
                  }
                }
                if (pythonic::builtins::pythran::and_([&] () { return pythonic::operator_::gt(ik1, 0L); }, [&] () { return pythonic::operator_::lt(ik1, pythonic::operator_::functor::floordiv()(nk1_min, 2L)); }))
                {
                  field_fft_out[pythonic::types::make_tuple(ik0, pythonic::operator_::neg(ik1), ik2)] = field_fft_in[pythonic::types::make_tuple(ik0, pythonic::operator_::neg(ik1), ik2)];
                }
              }
            }
          }
        }
      }
    }
    return pythonic::builtins::None;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_mini_oper_modif_resol::__transonic__()());
inline
typename __pythran_mini_oper_modif_resol::fill_field_fft_3d::type<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type fill_field_fft_3d0(pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& field_fft_in, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& field_fft_out) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_mini_oper_modif_resol::fill_field_fft_3d()(field_fft_in, field_fft_out);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_fill_field_fft_3d0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    
    char const* keywords[] = {"field_fft_in", "field_fft_out",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords , &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[1]))
        return to_python(fill_field_fft_3d0(from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_fill_field_fft_3d(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_fill_field_fft_3d0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "fill_field_fft_3d", "\n""    - fill_field_fft_3d(complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "fill_field_fft_3d",
    (PyCFunction)__pythran_wrapall_fill_field_fft_3d,
    METH_VARARGS | METH_KEYWORDS,
    "Fill the values from field_fft_in in field_fft_out\n""\n""    Supported prototypes:\n""\n""    - fill_field_fft_3d(complex128[:,:,:], complex128[:,:,:])\n""\n""    This function is specialized for FFTW3DReal2Complex (no MPI).\n"""},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "mini_oper_modif_resol",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(mini_oper_modif_resol)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(mini_oper_modif_resol)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("mini_oper_modif_resol",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.11.0",
                                      "2022-02-04 12:30:15.965747",
                                      "4e3e522a3258f8c13ce484c6de479a5cc8397877b5b4534a7454e5a0e09cdd03");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PyModule_AddObject(theModule, "__transonic__", __transonic__);
    PYTHRAN_RETURN;
}

#endif