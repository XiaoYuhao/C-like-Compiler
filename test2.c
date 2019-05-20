int d;
int func(int g,int f){
	int a;
	int b;
	a=2;
	b=g+f;
	b=b*a;
	return b;
}
int main(void){
	int a;
	int a;			//variable 'a' is redefined
	int b;
	int c;
	a=1;
	b=2;
	c=a+b;
	while(a<12)		//absence of a ';'
		a=a+1		//the left bracket symbol({) is missing	
	}
	if(c<10){
		c=a;
	}
	else{
		b=a;
	}
	b=func(a,c);
	return b;
}


