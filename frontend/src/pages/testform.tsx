import { useForm, SubmitHandler } from 'react-hook-form';
import Button from '../components/buttons/Button';
import TextInput from '../components/form-inputs/TextInput';
import Layout from '../components/layouts/Main';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';

type Inputs = {
  example: string;
  exampleRequired: string;
};

const schema = Yup.object({
  fname: Yup.string().required(),
  lname: Yup.string().required(),
});

const TestForm = () => {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    getValues,
  } = useForm<Inputs>({ resolver: yupResolver(schema) });

  const onSubmit: SubmitHandler<Inputs> = (data) => getValues();
  // console.log(watch('example'));
  console.log(errors);
  return (
    <Layout title="lsdkfj" heading="Test form">
      <section>
        <div className="container py-4">
          <form onSubmit={handleSubmit(onSubmit)}>
            <TextInput
              id="fname-id"
              label="First Name"
              name="fname"
              register={register}
              errors={errors}
              required
              placeholder="put your name here"
            />
            <TextInput
              id="lname-id"
              name="lname"
              label="Last Name"
              register={register}
              errors={errors}
              onChange={() => console.log('changed!')}
            />
            {/* // <input
            //   className="border block my-2"
            //   defaultValue="test"
            //   {...register('example')}
            // />
            <input
              className="border block my-2"
              {...register('exampleRequired', { required: true })}
            /> */}
            {/* {errors.exampleRequired && (
              <span className="block text-red-500">This field is required</span>
            )} */}
            <Button type="submit">Submit</Button>
          </form>
        </div>
      </section>
    </Layout>
  );
};
export default TestForm;
