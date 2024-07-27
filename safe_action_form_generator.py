import streamlit as st
from utils import generate_zod_schema

def generate_server_action(action_name, fields):
    schema = generate_zod_schema("object", fields)
    
    return f"""import {{ z }} from 'zod';
import {{ createSafeAction }} from 'next-safe-action';

{schema}

export const {action_name} = createSafeAction(schema, async (data) => {{
  // TODO: Implement your server-side logic here
  console.log('Received data:', data);

  // Simulating an asynchronous operation
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Return a success response
  return {{ message: 'Form submitted successfully' }};
}});
"""

def generate_form_component(form_name, fields):
    form_fields = "".join([f"""
        <FormField
          control={{form.control}}
          name="{field[0]}"
          render={{{{ field }} => (
            <FormItem>
              <FormLabel>{field[0].capitalize()}</FormLabel>
              <FormControl>
                <Input {{...field}} type="{field[1]}" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}}
        />""" for field in fields])

    return f"""'use client'

import {{ useForm }} from 'react-hook-form';
import {{ zodResolver }} from '@hookform/resolvers/zod';
import {{ useAction }} from 'next-safe-action/hook';
import {{ {form_name} as {form_name}Action }} from './server-actions';
import {{ z }} from 'zod';
import {{ Button }} from "@/components/ui/button"
import {{
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
}} from "@/components/ui/form"
import {{ Input }} from "@/components/ui/input"
import {{ useToast }} from "@/components/ui/use-toast"

const formSchema = z.object({{
  {", ".join([f"{field[0]}: z.string().min(1, '{{field[0].capitalize()}} is required')" for field in fields])}
}});

type FormData = z.infer<typeof formSchema>;

export function {form_name}Form() {{
  const form = useForm<FormData>({{
    resolver: zodResolver(formSchema),
    defaultValues: {{
      {", ".join([f"{field[0]}: ''" for field in fields])}
    }},
  }});

  const {{ execute, status }} = useAction({form_name}Action);
  const {{ toast }} = useToast();

  const onSubmit = async (data: FormData) => {{
    const result = await execute(data);
    if (result.data) {{
      toast({{
        title: "Success",
        description: result.data.message,
      }});
      form.reset();
    }} else if (result.validationErrors) {{
      // Handle validation errors
      Object.entries(result.validationErrors).forEach(([key, value]) => {{
        form.setError(key as any, {{
          type: "manual",
          message: value as string,
        }});
      }});
    }}
  }};

  return (
    <Form {{...form}}>
      <form onSubmit={{form.handleSubmit(onSubmit)}} className="space-y-8">
        {form_fields}
        <Button type="submit" disabled={{status === 'executing'}}>
          {{status === 'executing' ? 'Submitting...' : 'Submit'}}
        </Button>
      </form>
    </Form>
  );
}}
"""

def safe_action_form_page():
    st.header("Next.js Safe Action Form Generator (with React Hook Form and Shadcn UI)")

    form_name = st.text_input("Enter form name:", "ContactForm")

    num_fields = st.number_input("Number of fields:", min_value=1, value=3)

    fields = []
    for i in range(num_fields):
        col1, col2 = st.columns(2)
        with col1:
            field_name = st.text_input(f"Field {i+1} name:", f"field{i+1}")
        with col2:
            field_type = st.selectbox(f"Field {i+1} type:", ["text", "email", "number", "tel"], key=f"field_type_{i}")
        fields.append((field_name, field_type))

    if st.button("Generate Next.js Safe Action Form"):
        server_action_content = generate_server_action(form_name, fields)
        form_component_content = generate_form_component(form_name, fields)

        st.subheader("Server Action File (server-actions.ts)")
        st.code(server_action_content, language="typescript")
        
        st.subheader("Form Component File (form.tsx)")
        st.code(form_component_content, language="typescript")
        
        if st.button("Save Generated Files"):
            with open(f'{form_name.lower()}_server_actions.ts', 'w') as f:
                f.write(server_action_content)
            with open(f'{form_name.lower()}_form.tsx', 'w') as f:
                f.write(form_component_content)
            st.success(f"Files saved as {form_name.lower()}_server_actions.ts and {form_name.lower()}_form.tsx")

if __name__ == "__main__":
    safe_action_form_page()