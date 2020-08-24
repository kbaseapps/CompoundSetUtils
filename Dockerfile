FROM kbase/sdkbase2:python
MAINTAINER KBase Developer2
# -----------------------------------------
RUN apt-get update -y && \
    apt-get install -y wget openbabel

RUN conda config --add channels  https://conda.anaconda.org/rdkit && \
    conda install -y nose \
                     cairo \
                     nomkl \
                     rdkit

RUN pip install --upgrade pip && \
    pip install jinja2 requests jsonrpcbase

RUN curl --location http://mgltools.scripps.edu/downloads/downloads/tars/releases/REL1.5.6/mgltools_x86_64Linux2_1.5.6.tar.gz > mgltools.tar.gz && \
tar vxzf mgltools.tar.gz && \                                                                       
rm mgltools.tar.gz && \                                                                             
mv mgltools_x86_64Linux2_1.5.6 /usr/local/lib/ && \                                                  
cd /usr/local/lib/mgltools_x86_64Linux2_1.5.6 && \                                                  
./install.sh                                                                                        
                                                                                                    
ENV PATH="${PATH}:/usr/local/lib/mgltools_x86_64Linux2_1.5.6/bin" 


COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module
WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
